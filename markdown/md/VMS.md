# VMS 使用说明

## 引入方式
依赖的jar包为android.car.jar。

``` gradle
dependencies {
    implementation files('libs/android.car.jar')
}
```

需要申请权限Car.PERMISSION_VMS_PUBLISHER和(或)Car.PERMISSION_VMS_SUBSCRIBER。

``` xml
<uses-permission android:name="android.car.permission.VMS_PUBLISHER" />
<uses-permission android:name="android.car.permission.VMS_SUBSCRIBER" />
```

## 示例代码
### 订阅者
``` java
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import android.car.vms.VmsLayer;
import com.neu.ac.vms.Vms;
import com.neu.ac.vms.VmsManager;

public class VMSActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 取得manager
        VmsManager manager = new VmsManager(this);

        // 注册回调函数
        manager.registerPacketCallback((layer, packet) -> {
            // 作为例子，这里只是简单地打印一下log
            Log.i("AVM", packet);
            // 你的回调函数应该包含针对具体消息的具体处理
        });

        // 如果你是订阅者，你可能希望订阅一些消息
        manager.getClient()
                .setSubscriptions(Vms.LAYER_AUDIO_FOCUS);
    }

    @Override
    protected void onDestroy() {
        // 移除回调函数
        manager.unregisterPacketCallback();

        super.onDestroy();
    }
}
```
### 发布者
``` java
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import android.car.vms.VmsLayer;
import com.neu.ac.vms.Vms;
import com.neu.ac.vms.VmsManager;

public class VMSActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 取得manager
        VmsManager manager = new VmsManager(this);
        
        // 如果你是发布者，你可能希望发布一些消息，可以级联调用
        manager.getClient()
                .setProviderOfferings(Vms.LAYER_AUDIO_FOCUS)
                .publishPacket(Vms.LAYER_AUDIO_FOCUS, "hello world");
    }
}
```
消息格式请参考 [VMS功能参数对照表.xlsx](http://10.1.55.36/svn/AndroidPF/04.SoftwareDevelopLibrary/03.SystemDesign(SD)/AndroidPF_Dev/02.InterfaceDefinition/VMS%E5%8A%9F%E8%83%BD%E5%8F%82%E6%95%B0%E5%AF%B9%E7%85%A7%E8%A1%A8.xlsx)
