class MerryMimetype:

    def __init__(self, _type, tail):

        self._type = _type
        self.tail = tail

    def __str__(self) -> str:
            return f"{self._type}/{self.tail}"

class MerryMimetypes:

    aac: MerryMimetype = MerryMimetype("audio", "aac")
    abw: MerryMimetype = MerryMimetype("application", "x-abiword")
    arc: MerryMimetype = MerryMimetype("application", "x-freearc")
    avif: MerryMimetype = MerryMimetype("image", "avif")
    avi: MerryMimetype = MerryMimetype("video", "x-msvideo")
    azw: MerryMimetype = MerryMimetype("application", "vnd.amazon.ebook")
    bin: MerryMimetype = MerryMimetype("application", "octet-stream")
    bmp: MerryMimetype = MerryMimetype("image", "bmp")
    bz: MerryMimetype = MerryMimetype("application", "x-bzip")
    bz2: MerryMimetype = MerryMimetype("application", "x-bzip2")
    cda: MerryMimetype = MerryMimetype("application", "x-cdf")
    csh: MerryMimetype = MerryMimetype("application", "x-csh")
    css: MerryMimetype = MerryMimetype("text", "css")
    csv: MerryMimetype = MerryMimetype("text", "csv")
    doc: MerryMimetype = MerryMimetype("application", "msword")
    docx: MerryMimetype = MerryMimetype("application", "vnd.openxmlformats-officedocument.wordprocessingml.document")
    eot: MerryMimetype = MerryMimetype("application", "vnd.ms-fontobject")
    epub: MerryMimetype = MerryMimetype("application", "epub+zip")
    gz: MerryMimetype = MerryMimetype("application", "gzip")
    gif: MerryMimetype = MerryMimetype("image", "gif")
    htm: MerryMimetype = MerryMimetype("text", "html")
    html: MerryMimetype = MerryMimetype("text", "html")
    ico: MerryMimetype = MerryMimetype("image", "vnd.microsoft.icon")
    ics: MerryMimetype = MerryMimetype("text", "calendar")
    jar: MerryMimetype = MerryMimetype("application", "java-archive")
    jpeg: MerryMimetype = MerryMimetype("image", "jpeg")
    jpg: MerryMimetype = MerryMimetype("image", "jpeg")
    js: MerryMimetype = MerryMimetype("text", "javascript")
    json: MerryMimetype = MerryMimetype("application", "json")
    jsonld: MerryMimetype = MerryMimetype("application", "ld+json")
    mid: MerryMimetype = MerryMimetype("audio", "midi")
    midi: MerryMimetype = MerryMimetype("audio", "midi")
    mjs: MerryMimetype = MerryMimetype("text", "javascript")
    mp3: MerryMimetype = MerryMimetype("audio", "mpeg")
    mp4: MerryMimetype = MerryMimetype("video", "mp4")
    mpeg: MerryMimetype = MerryMimetype("video", "mpeg")
    mpkg: MerryMimetype = MerryMimetype("application", "vnd.apple.installer+xml")
    odp: MerryMimetype = MerryMimetype("application", "vnd.oasis.opendocument.presentation")
    ods: MerryMimetype = MerryMimetype("application", "vnd.oasis.opendocument.spreadsheet")
    odt: MerryMimetype = MerryMimetype("application", "vnd.oasis.opendocument.text")
    oga: MerryMimetype = MerryMimetype("audio", "ogg")
    ogv: MerryMimetype = MerryMimetype("video", "ogg")
    ogx: MerryMimetype = MerryMimetype("application", "ogg")
    opus: MerryMimetype = MerryMimetype("audio", "opus")
    otf: MerryMimetype = MerryMimetype("font", "otf")
    png: MerryMimetype = MerryMimetype("image", "png")
    pdf: MerryMimetype = MerryMimetype("application", "pdf")
    php: MerryMimetype = MerryMimetype("application", "x-httpd-php")
    ppt: MerryMimetype = MerryMimetype("application", "vnd.ms-powerpoint")
    pptx: MerryMimetype = MerryMimetype("application", "vnd.openxmlformats-officedocument.presentationml.presentation")
    rar: MerryMimetype = MerryMimetype("application", "vnd.rar")
    rtf: MerryMimetype = MerryMimetype("application", "rtf")
    sh: MerryMimetype = MerryMimetype("application", "x-sh")
    svg: MerryMimetype = MerryMimetype("image", "svg+xml")
    tar: MerryMimetype = MerryMimetype("application", "x-tar")
    tif: MerryMimetype = MerryMimetype("image", "tiff")
    tiff: MerryMimetype = MerryMimetype("image", "tiff")
    ts: MerryMimetype = MerryMimetype("video", "mp2t")
    ttf: MerryMimetype = MerryMimetype("font", "ttf")
    txt: MerryMimetype = MerryMimetype("text", "plain")
    vsd: MerryMimetype = MerryMimetype("application", "vnd.visio")
    wav: MerryMimetype = MerryMimetype("audio", "wav")
    weba: MerryMimetype = MerryMimetype("audio", "webm")
    webm: MerryMimetype = MerryMimetype("video", "webm")
    webp: MerryMimetype = MerryMimetype("image", "webp")
    woff: MerryMimetype = MerryMimetype("font", "woff")
    woff2: MerryMimetype = MerryMimetype("font", "woff2")
    xhtml: MerryMimetype = MerryMimetype("application", "xhtml+xml")
    xls: MerryMimetype = MerryMimetype("application", "vnd.ms-excel")
    xlsx: MerryMimetype = MerryMimetype("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    xml: MerryMimetype = MerryMimetype("application", "xml")
    xul: MerryMimetype = MerryMimetype("application", "vnd.mozilla.xul+xml")
    zip: MerryMimetype = MerryMimetype("application", "zip")
    _3gp: MerryMimetype = MerryMimetype("video", "3gpp")
    _3g2: MerryMimetype = MerryMimetype("video", "3gpp2")
    _7z: MerryMimetype = MerryMimetype("application", "x-7z-compressed")
    mimetypes = {
        "aac": aac,
        "abw": abw,
        "arc": arc,
        "avif": avif,
        "avi": avi,
        "azw": azw,
        "bin": bin,
        "bmp": bmp,
        "bz": bz,
        "bz2": bz2,
        "cda": cda,
        "csh": csh,
        "css": css,
        "csv": csv,
        "doc": doc,
        "docx": docx,
        "eot": eot,
        "epub": epub,
        "gz": gz,
        "gif": gif,
        "htm": htm,
        "html": html,
        "ico": ico,
        "ics": ics,
        "jar": jar,
        "jpeg": jpeg,
        "jpg": jpg,
        "js": js,
        "json": json,
        "jsonld": jsonld,
        "mid": mid,
        "midi": midi,
        "mjs": mjs,
        "mp3": mp3,
        "mp4": mp4,
        "mpeg": mpeg,
        "mpkg": mpkg,
        "odp": odp,
        "ods": ods,
        "odt": odt,
        "oga": oga,
        "ogv": ogv,
        "ogx": ogx,
        "opus": opus,
        "otf": otf,
        "png": png,
        "pdf": pdf,
        "php": php,
        "ppt": ppt,
        "pptx": pptx,
        "rar": rar,
        "rtf": rtf,
        "sh": sh,
        "svg": svg,
        "tar": tar,
        "tif": tif,
        "tiff": tiff,
        "ts": ts,
        "ttf": ttf,
        "txt": txt,
        "vsd": vsd,
        "wav": wav,
        "weba": weba,
        "webm": webm,
        "webp": webp,
        "woff": woff,
        "woff2": woff2,
        "xhtml": xhtml,
        "xls": xls,
        "xlsx": xlsx,
        "xml": xml,
        "xul": xul,
        "zip": zip,
        "3gp": _3gp,
        "3g2": _3g2,
        "7z": _7z,
    }

    @staticmethod
    def get_mime_type(mimetype):

        value = MerryMimetypes.mimetypes.get(mimetype)

        if value is not None:
            return value
        else:
            raise Exception("Unknown file type. Add mimeType argument.")

