# Volume

Car中所有音源的音量均通过硬件调整，而软件不做调整。

## 功能

### 1. 音量调整

| No.  | API                                                          | Comment                                   |
| ---- | ------------------------------------------------------------ | ----------------------------------------- |
| 1    | public void setGroupVolume(int groupId, int index, int flags) | 给primary zone的指定group设置指定的音量值 |
| 2    | public void setGroupVolume(int zoneId, int groupId, int index, int flags) | 给指定zone和group设置指定的音量值         |
| 3    | public void registerCarVolumeCallback(@NonNull CarVolumeCallback callback) | 注册CarVolumeCallback，用于监听音量变更   |
| 4    | public void unregisterCarVolumeCallback(@NonNull CarVolumeCallback callback) | 取消注册CarVolumeCallback                 |

### 2. 音量获取

| No.  | API                                                   | Comment                               |
| ---- | ----------------------------------------------------- | ------------------------------------- |
| 1    | public int getGroupMaxVolume(int groupId)             | 获取primary zone的指定group的最大音量 |
| 2    | public int getGroupMaxVolume(int zoneId, int groupId) | 获取指定zone和group的最大音量         |
| 3    | public int getGroupMinVolume(int groupId)             | 获取primary zone的指定group的最小音量 |
| 4    | public int getGroupMinVolume(int zoneId, int groupId) | 获取指定zone和group的最小音量         |
| 5    | public int getGroupVolume(int groupId)                | 获取primary zone的指定group的当前音量 |
| 6    | public int getGroupVolume(int zoneId, int groupId)    | 获取指定zone和group的当前音量         |

### 3. 设置静音/非静音

| No.  | API                                                          | Comment                                      |
| ---- | ------------------------------------------------------------ | -------------------------------------------- |
| 1    | public void setVolumeGroupMute(int zoneId, int groupId, boolean mute, int flags) | 给指定zone和group设置静音/取消静音（待实现） |
| 2    | public boolean isVolumeGroupMuted(int zoneId, int groupId)   | 是否静音（待实现）                           |

## 使用说明

### 引入方式

1. 依赖的jar包为android.car.jar

``` gradle
dependencies {
    implementation files('libs/android.car.jar')
}
```

2. 需要申请的权限

``` xml
<uses-permission android:name="android.car.permission.CAR_CONTROL_AUDIO_VOLUME" />
```

### 示例代码

```java
...
private CarAudioManager mCarAudioManager = null;
private TempCarVolumeCallback mCallback = null;
...

private final class TempCarVolumeCallback extends CarAudioManager.CarVolumeCallback {
        @Override
        public void onGroupVolumeChanged(int zoneId, int groupId, int flags) {
            Log.i(TAG, "onGroupVolumeChanged zoneId = " + zoneId + ", groupId" + groupId);
            //get current volume
            int volume = mCarAudioManager.getGroupVolume(zoneId, groupId);
            Log.i(TAG, "Volume changes to " + volume);
        }
    }
...
    
mCarAudioManager = (CarAudioManager) mCar.getCarManager(Car.AUDIO_SERVICE);
mCallback = new TempCarVolumeCallback();
//Register callback for volume change.
mCarAudioManager.registerCarVolumeCallback(mCallback);
...

//set media volume to 30
int groupId = mCarAudioManager.getVolumeGroupIdForUsage(AudioAttributes.USAGE_MEDIA);
mCarAudioManager.setGroupVolume(groupId, 30, 0); 

```

