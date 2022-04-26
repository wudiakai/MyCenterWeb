# Effect

## 功能

### 1.平衡设置

| No.  | API                                     | Comment                             |
| ---- | --------------------------------------- | ----------------------------------- |
| 1    | void setBalanceTowardRight(float value) | 用于控制车载音响设备的右/左平衡设置 |
| 2    | void setFadeTowardFront(float value)    | 用于控制车载音响设备的前/后淡化设置 |



### 2.音效设定

| No.  | API                           | Comment          |
| ---- | ----------------------------- | ---------------- |
| 1    | void setEffectMode(int style) | 用于设置音效模式 |

## 使用说明

### 引入方式

1. 依赖的jar包为android.car.jar

```html
dependencies {
    implementation files('libs/android.car.jar')
}
```

2. 需要申请的权限

```html
<uses-permission android:name="android.car.permission.CAR_CONTROL_AUDIO_VOLUME" />
```

示例代码

```java
...
private CarAudioManager mCarAudioManager = null;
    
...
mCarAudioManager = (CarAudioManager) mCar.getCarManager(Car.AUDIO_SERVICE);

//set balance to left
mCarAudioManager.setBalanceTowardRight(-1.0);

//set sound effects to Jazz
mCarAudioManager.setEffectMode(AUDIO_EFFECT_STYLE_JAZZ);
```