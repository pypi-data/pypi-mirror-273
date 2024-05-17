import json
import os
import pathlib
import requests
import sys
import socket

from typing import Callable, Optional
from merrymake.streamhelper import read_to_end
from merrymake.nullmerrymake import NullMerrymake
from merrymake.imerrymake import IMerrymake
from merrymake.merrymimetypes import MerryMimetypes, MerryMimetype
from merrymake.envelope import Envelope

tcp = False

class Merrymake(IMerrymake):
    """Merrymake is the main class of this library, as it exposes all other
     functionality, through a builder pattern.

     @author Merrymake.eu (Chirstian Clausen, Nicolaj Græsholt)
    """

    @staticmethod
    def service():
        """This is the root call for a Merrymake service.

        Returns
        -------
        A Merrymake builder to make further calls on
        """

        args = sys.argv[1:]
        return Merrymake(args)

    def __init__(self, args):
        global tcp
        try:
            if len(args) == 0:
                tcp = True
                buffer = read_to_end(sys.stdin.buffer)
                st = 0
                actionLen = (buffer[st+0]<<16) | (buffer[st+1]<<8) | buffer[st+2]
                st += 3
                self.action = bytes(buffer[st:st+actionLen]).decode('utf-8')
                st += actionLen
                envelopeLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
                st += 3
                buf = json.loads(bytes(buffer[st:st+envelopeLen]).decode('utf-8'));
                self.envelope = Envelope(buf.get("messageId"), buf.get("traceId"), buf.get("sessionId"))
                st += envelopeLen
                payloadLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
                st += 3
                self.payloadBytes = bytes(buffer[st:st+payloadLen])
            else:
                self.action = args[-2]
                buf = json.loads(args[-1])
                self.envelope = Envelope(buf.get("messageId"), buf.get("traceId"), buf.get("sessionId"))
                self.payloadBytes = read_to_end(sys.stdin.buffer)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            raise Exception("Decoding JSON has failed")
        except:
            print("Could not read from stdin")
            raise Exception("Could not read from stdin")

    def handle(self, action: str, handler: Callable[[bytearray, Envelope], None]):
        if self.action == action:
            handler(self.payloadBytes, self.envelope)
            return NullMerrymake()
        else:
            return self

    def initialize(self, f: Callable[[], None]):
        f()

    @staticmethod
    def post_event_to_rapids(pEvent: str):
        """Post an event to the central message queue (Rapids), without a payload.

        Parameters
        ----------
        event : string
            The event to post
        """

        uri = f"{os.getenv('RAPIDS')}/{pEvent}"
        requests.post(uri)

    @staticmethod
    def post_to_rapids(pEvent: str, body: bytes | str | dict):
        """Post an event to the central message queue (Rapids), with a payload and its
         content type.

        Parameters
        ----------
        event : string
            The event to post
        body : string
            The payload
        contentType : MimeType
            The content type of the payload
        """

        global tcp
        if tcp:
            if pEvent == "$reply":
                body["headers"]["contentType"] = body["headers"]["content_type"].__str__()
                del body["headers"]["content_type"]
            parts = os.getenv('RAPIDS').split(":")
            with socket.socket() as s:
                s.connect((parts[0], int(parts[1])))
                byteBody = bytes(json.dumps(body), 'utf-8') if type(body) is dict else bytes(body, 'utf-8') if type(body) is str else body
                eventLen = len(pEvent)
                byteBodyLen = len(byteBody)
                s.sendall(bytes([eventLen>>16, eventLen>>8, eventLen>>0]))
                s.sendall(bytes(pEvent, 'utf-8'))
                s.sendall(bytes([byteBodyLen>>16, byteBodyLen>>8, byteBodyLen>>0]))
                s.sendall(byteBody)
        else:
            if pEvent == "$reply":
                headers = { 'Content-Type': body["headers"]["content_type"].__str__() }
                body = body["content"]
            elif type(body) is str:
                headers = { 'Content-Type': "text/plain" }
            else:
                headers = { 'Content-Type': "application/json" }
                body = json.dumps(body)
            uri = f"{os.getenv('RAPIDS')}/{pEvent}"

            requests.post(uri, data=body, headers=headers)

    @staticmethod
    def reply_to_origin(body: str, content_type: MerryMimetype):
        """Post a reply back to the originator of the trace, with a payload and its
         content type.

        Parameters
        ----------
        body : string
            The payload
        contentType : MimeType
            The content type of the payload
        """

        Merrymake.post_to_rapids("$reply", {"content": body, "headers": { "content_type": content_type }})

    @staticmethod
    def reply_file_to_origin(path: str):
        """Send a file back to the originator of the trace.

        Parameters
        ----------
        path : string
            The path to the file
        """

        # get the extension, skip the dot
        extension = pathlib.Path(path).suffix[1:]

        mime = MerryMimetypes.get_mime_type(extension)

        Merrymake.reply_file_to_origin_with_content_type(path, mime)

    @staticmethod
    def reply_file_to_origin_with_content_type(path: str, content_type: MerryMimetype):
        """Send a file back to the originator of the trace.

        Parameters
        ----------
        path : string
            The path to the file starting from main/resources
        contentType : MimeType
            The content type of the file
        """
        with open(path, 'r') as file:
            body = file.read()
            Merrymake.reply_to_origin(body, content_type)

    @staticmethod
    def join_channel(channel: str):
        """Subscribe to a channel
        Events will stream back messages broadcast to that channel. You can join multiple channels. You stay in the channel until the
        request is terminated.

        Note: The origin-event has to be set as "streaming: true" in the
        event-catalogue.

        Parameters
        ----------
        channel : string
            The channel to join
        """

        Merrymake.post_to_rapids("$join", channel)

    @staticmethod
    def broadcast_to_channel(to: str, event: str, payload: str):
        """Broadcast a message (event and payload) to all listeners in a channel.

        Parameters
        ----------
        to : string
            The channel to broadcast to
        event : string
            The event-type of the message
        payload : string
            The payload of the message
        """

        Merrymake.post_to_rapids("$broadcast", {"to": to, "event": event, "payload": payload})
