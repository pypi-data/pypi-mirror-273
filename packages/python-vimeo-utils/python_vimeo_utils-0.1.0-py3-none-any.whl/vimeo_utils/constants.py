class TranscodeStatus:
    COMPLETE = "complete"
    ERROR = "error"
    IN_PROGRESS = "in_progress"


class VideoStatus:
    AVAILABLE = "available"
    TRANSCODE_STARTING = "transcode_starting"
    TRANSCODING = "transcoding"
    TRANSCODING_ERROR = "transcoding_error"
    UNAVAILABLE = "unavailable"
    UPLOADING = "uploading"
    UPLOADING_ERROR = "uploading_error"
