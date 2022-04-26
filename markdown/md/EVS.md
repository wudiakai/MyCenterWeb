# EVS 使用说明

## 概述
EVS模块负责接收各种外部视频流，并提供了方便的接口将其展示给用户。
各外部视频流对应的具体设备可通过配置文件配置，并可在运行时切换。

## 配置
请 overlay `packages/services/Car/service/res/values/config.xml`。
具体配置项如下:
``` xml
<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
    <!-- A name of a camera device that provides the rearview through EVS service -->
    <string name="config_evsRearviewCameraId" translatable="false">/dev/video2</string>
    <string name="config_evsFrontviewCameraId" translatable="false">/dev/video4</string>
    <string name="config_evsAvmviewCameraId" translatable="false">/dev/video2</string>
    <string name="config_evsHdmiviewCameraId" translatable="false">/dev/video2</string>
    <string name="config_evsDvrviewCameraId" translatable="false">/dev/video2</string>
    <string name="config_evsDvdviewCameraId" translatable="false">/dev/video2</string>

    <!-- The camera Activity name for EVS, if defined, the Activity will be launched by CarEvsService. -->
    <string name="config_evsCameraActivity" translatable="false"></string>
</resources>
```
其中第一段用来配置各视频源对应的设备，目前支持的视频源有前视、后视、AVM、HDMI、DVR、DVD。
第二段的配置项是车辆挂入倒车档时要启动的app。


## 引入方式
依赖的jar包为android.car.jar。

``` gradle
dependencies {
    implementation files('libs/android.car.jar')
}
```

需要申请权限USE_CAR_EVS_CAMERA。

``` xml
<uses-permission android:name="android.car.permission.USE_CAR_EVS_CAMERA" />
```

## 示例代码

``` java
import androidx.appcompat.app.AppCompatActivity;

import android.car.Car;
import android.os.Bundle;
import android.widget.Button;

import com.neu.ac.evs.EvsManager;
import com.neu.ac.evs.view.CarEvsCameraGLSurfaceView;

public class MainActivity extends AppCompatActivity {
    private Car mCar;
    private EvsManager mManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 取得Car
        mCar = Car.createCar(this);

        // 取得EvsManager
        mManager = new EvsManager(mCar);

        // 打开指定的视频流
        mManager.startVideoStream(EvsManager.EVS_TYPE_REARVIEW);

        // 取得evsView
        CarEvsCameraGLSurfaceView evsView = findViewById(R.id.evsView);

        // 将manager传给evsView进行描画
        evsView.initRender(mManager);

        Button stopButton = findViewById(R.id.stopButton);
        stopButton.setOnClickListener(v -> finish());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // 退出时记得关闭流
        mManager.stopVideoStream();

        // 并断开与Car的连接
        mCar.disconnect();
    }
}
```

### 布局
``` xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <com.neu.ac.evs.view.CarEvsCameraGLSurfaceView
        android:id="@+id/evsView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <Button
        android:id="@+id/stopButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Stop"
        app:layout_constraintBottom_toBottomOf="@+id/evsView"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

## 高级用法

以下功能请参本EVS模块的API文档了解更详细的参数。

### 叠加描画内容
我们提供了`CarEvsCameraGLSurfaceView`以方便开发者进行快速的描画，如上述例子所示，只需将`EvsManager`传入该View的`initRender()`方法，并启动指定的视频流，即可在该View上看到相应的画面。

`initRender()`方法还提供第二个参数，该参数是一个回调函数，用于在视频数据描画完成后叠加自定义的描画动作。你可以使用这个功能在视频上描画其它内容，例如辅助线或是提示文字、图标等。

### 自定义Buffer处理
上述例子中，直接使用`CarEvsCameraGLSurfaceView`将buffer用于描画。实际上，你还可以使用buffer做任何你想做的事情，例如将其用于你自己的View，或是自行处理buffer数据等等。

通过调用`getNewFrame()`，你可以随时取得新的buffer用于自己的处理。不过在使用完这个buffer后，一定要记得调用`returnBuffer(buffer)`进行归还。

### 视频切换
在视频流处理过程中，你可以随时调用`startVideoStream(type)`函数来切换另一个视频流，且无须关闭先前的流。实际上，由于EVS服务当前并不支持同时打开多个视频流，所以打开新的视频流会自动关闭旧的。

不过，在使用流的View被销毁，或是你的应用退出时，请记得关闭最后的流，并断开与`Car`的连接，否则可能导致资源泄露问题。

### 底层配置
```xml
<?xml version='1.0' encoding='utf-8'?>
<configuration>
    <!-- system configuration -->
    <system>
        <!-- number of cameras available to EVS -->
        <num_cameras value='2'/>
    </system>
    <!-- camera device information -->
    <camera>
        <!-- camera group 0 -->
        <!-- group id='group0' synchronized='APPROXIMATE' -->
        <group id='group0' synchronized='CALIBRATED'>
            <caps>
            </caps>
            <!-- list of parameters -->
            <characteristics>
            </characteristics>
        </group>
        <!-- camera device starts -->
        <device id='/dev/video3' position='rear'>
            <caps>
                <!-- list of supported controls -->
                <supported_controls>
                    <control name='BRIGHTNESS' min='0' max='255'/>
                    <control name='CONTRAST' min='0' max='255'/>
                    <control name='ABSOLUTE_FOCUS' min='0' max='255' step='5'/>
                </supported_controls>
                <!-- list of supported stream configurations -->
                <stream id='0' width='1920' height='1080' format='RGBA_8888' framerate='5'/>
                <stream id='1' width='2304' height='1296' format='RGBA_8888' framerate='2'/>
            </caps>
            <!-- list of parameters -->
            <characteristics>
                <parameter
                    name='LENS_DISTORTION'
                    type='float'
                    size='5'
                    value='0.0,0.0,0.0,0.0,0.0'
                />
            </characteristics>
        </device>
    </camera>
    <!-- display device starts -->
    <display>
        <device id='display0'>
        </device>
    </display>
</configuration>
```
底层配置主要分为三部分，`system`，`camera`和`display`。其中`system`很简单，请参考上述片断。`camera`可包含多个`group`和`device`。`group`可以理解为一种由多个`device`组成的特殊`device`。`device`又由`caps`和`characteristics`组成。以下展开说明`caps`和`characteristics`。

`caps`描述指定摄像头的能力，其又分为`supported_controls`和`stream`两项。这些参数可以由`v4l2-ctl`命令查询得到。

`control`的每一项由`name`、`min`、`max`和可选的`step`组成，用于指定某个特定控制参数的范围。`name`的可能值为:
- BRIGHTNESS
- CONTRAST
- AUTOGAIN
- GAIN
- AUTO_WHITE_BALANCE
- WHITE_BALANCE_TEMPERATURE
- SHARPNESS
- AUTO_EXPOSURE
- ABSOLUTE_EXPOSURE
- ABSOLUTE_FOCUS
- AUTO_FOCUS
- ABSOLUTE_ZOOM


`stream`则由`id`、`width`、`height`、`format`、`framerate`构成,支持的`format`包括:
- RGBA_8888
- YCRCB_420_SP
- YCBCR_422_I


`characteristics`则是一些标定相关的参数。每个`parameter`由`name`、`type`、`size`和`value`组成。`name`的可能值为:
- LENS_DISTORTION (float[])
- LENS_INTRINSIC_CALIBRATION (float[])
- LENS_POSE_ROTATION (float[])
- LENS_POSE_TRANSLATION (float[])
- REQUEST_AVAILABLE_CAPABILITIES (char*)
    - DEPTH_OUTPUT
    - LOGICAL_MULTI_CAMERA
    - MONOCHROME
    - SECURE_IMAGE_DATA
- LOGICAL_MULTI_CAMERA_PHYSICAL_IDS (char*)
