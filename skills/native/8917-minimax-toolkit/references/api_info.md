# MiniMax API Info (Token Plan Plus)

## Model IDs

| Modality | Flagship Model | Alternative / Specialized |
| :--- | :--- | :--- |
| **Text** | `MiniMax-M2.7-highspeed` | `MiniMax-M2.7`, `M2-her` |
| **Image** | `image-01` | `image-01-live` (Anime/Cartoon style) |
| **Video** | `MiniMax-Hailuo-02` | `MiniMax-Hailuo-2.3` |
| **Speech** | `speech-2.8-hd` | `speech-2.8-turbo`, `speech-2.6-hd` |
| **Music** | `music-2.5+` | `music-2.5` |

## Voice IDs (Speech Synthesis)

- `male-qn-qingse` (Default)
- `Chinese (Mandarin)_Lyrical_Voice`
- `English_Graceful_Lady`
- ... (Refer to MiniMax dashboard for full list)

## Key Constraints

- **Request Units**: Token Plan uses a "Request" unit system.
- **Quota**: 5-hour rolling window.
- **Consumption Rate**:
    - Text: 1 Unit / call
    - Image: 75 Units / image
    - Video (Hailuo-02): 4500 Units / 6s video
    - Speech (HD): 600 Units / 1000 characters
    - Music (2.5+): 3000 Units / 5min song
