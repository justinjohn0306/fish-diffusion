import torch
from torchaudio.transforms import MelSpectrogram


def dynamic_range_compression(x, C=1, clip_val=1e-5):
    """
    PARAMS
    ------
    C: compression factor
    """

    return torch.log(torch.clamp(x, min=clip_val) * C)


def dynamic_range_decompression(x, C=1):
    """
    PARAMS
    ------
    C: compression factor used to compress
    """

    return torch.exp(x) / C


@torch.no_grad()
def get_mel_from_audio(
    audio: torch.Tensor,
    sample_rate=44100,
    n_fft=2048,
    win_length=2048,
    hop_length=512,
    f_min=40,
    f_max=16000,
    n_mels=128,
    center=True,
    power=1.0,
    pad_mode="reflect",
    norm="slaney",
    mel_scale="slaney",
) -> torch.Tensor:
    """Get mel spectrogram from audio

    Args:
        audio (torch.Tensor): audio tensor (1, n_samples)

    Returns:
        torch.Tensor: mel spectrogram (n_mels, n_frames)
    """

    assert audio.ndim == 2, "Audio tensor must be 2D (1, n_samples)"
    assert audio.shape[0] == 1, "Audio tensor must be mono"

    transform = MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=n_fft,
        win_length=win_length,
        hop_length=hop_length,
        f_min=f_min,
        f_max=f_max,
        n_mels=n_mels,
        center=center,
        power=power,
        pad_mode=pad_mode,
        norm=norm,
        mel_scale=mel_scale,
    ).to(audio.device)

    mel = transform(audio)
    mel = dynamic_range_compression(mel)

    return mel[0]
