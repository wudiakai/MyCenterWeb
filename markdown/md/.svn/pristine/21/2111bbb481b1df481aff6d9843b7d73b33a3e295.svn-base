# AudioFocus

## 功能

### 1.获取音频焦点

| No.  | API                                                          | Comment          |
| ---- | ------------------------------------------------------------ | ---------------- |
| 1    | public int requestAudioFocus(@NonNull AudioFocusRequest focusRequest) | 请求取得音频焦点 |

### 2.释放音频焦点

| No.  | API                                                          | Comment      |
| ---- | ------------------------------------------------------------ | ------------ |
| 1    | public int abandonAudioFocusRequest(@NonNull AudioFocusRequest focusRequest) | 释放音频焦点 |

## 使用说明

### 引入方式

依赖的jar包为android.car.jar

```gradle
dependencies {
    implementation files('libs/android.car.jar')
}
```

### 配置焦点关联矩阵

在使用Car版音频焦点管理时，需要将焦点关联矩阵interaction_matrix_configuration.xml 配置到指定目录下。例如，（***需修改，要求统一放到common模块***）

```html
PRODUCT_COPY_FILES += \
vendor/naaivi/hardware/libhardware/audio/configs/interaction_matrix_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/interaction_matrix_configuration.xml \
```

### 配置Duck矩阵

在抢占音频焦点时，如果音源间需要混音，那么就需要配置Duck矩阵contexts_to_duck_configuration.xml 。配置方法是需要将其放置到指定目录下，例如，（***需修改，要求统一放到common模块***）

```html
PRODUCT_COPY_FILES += \
vendor/naaivi/hardware/libhardware/audio/configs/contexts_to_duck_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/contexts_to_duck_configuration.xml \
```

### 示例代码

```java
  ...
  mPlaybackAttributes = new AudioAttributes.Builder()
           .setUsage(AudioAttributes.USAGE_NOTIFICATION)
           .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
           .build();
  AudioFocusRequest focusRequest = new AudioFocusRequest.Builder(
           AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
           .setAudioAttributes(mPlaybackAttributes)
           .setOnAudioFocusChangeListener(this, new Handler())
           .build();
  mAudiofocusRequestFailed = mAudioManager.requestAudioFocus(focusRequest);
  if (mAudiofocusRequestFailed == AudioManager.AUDIOFOCUS_REQUEST_GRANTED) {
       // Only play the sound if we actually gained audio focus.
       mPlayer.start();
  } else {
       cleanUp();
  }
  ...
```

