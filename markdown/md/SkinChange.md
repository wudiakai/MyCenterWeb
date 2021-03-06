# **换肤功能使用说明**

# 一、皮肤包的制作

## 1. 创建皮肤包工程

1. 进入统一存放换肤包的Android源码工程目录：`AndroidPF/apps/LINUX/android/vendor/naaivi/external/skins/`

2. 创建相应主题的app的皮肤包。例如：在Blue主题下创建Audio的皮肤包工程，目录结构如下

   `└── skins
       ├── Blue
       │   └── Audio
       │       ├── AndroidMainfest.xml
       │       ├── Android.mk
       │       └── res
       │           └── values
       │           └── drawable-mdpi`

## 2. 创建清单文件、makefile文件

1. 编辑AndroidMainfest.xml文件。文件内容可参考下述代码：

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.neusoft.audio.skin.blue" >

    <overlay android:targetPackage="com.neusoft.audio" android:priority="1"/>

    <application
            android:hasCode="false" >
    </application>
</manifest>

<!-- 
属性说明：
targetPackage：需要换肤目标app的包名
priority：当多个静态叠加层以相同的资源值为替换目标时，此数字属性的值（仅影响静态叠加层）将配置叠加层的优先级。数值越大表示优先级越高。
hasCode：由于无法叠加代码，因此叠加层无法使用 DEX 文件。此外，必须将清单中 <application> 标记的 android:hasCode 属性设置为 false。
-->
```

2. 编辑Android.mk文件（可参考下述代码）

```makefile
include $(CLEAR_VARS)

LOCAL_MODULE_TAGS := optional
LOCAL_PACKAGE_NAME := com.neusoft.audio.skin.blue
LOCAL_CERTIFICATE := platform
LOCAL_SDK_VERSION := current
LOCAL_PROGUARD_ENABLED := disabled
LOCAL_DEX_PREOPT := false
LOCAL_MODULE_PATH  := $(TARGET_OUT_PRODUCT)/overlay/

include $(BUILD_PACKAGE)
```

## 3. 创建资源文件

1. 编辑res文件夹，并将需要替换的资源文件放入对应目录。
1. 需要注意的是资源文件的名称要与目标app所引用的文件名保持一致。



# 二、主题切换

SystemUI或Setting 主题切换功能的开发，可参照下述步骤

## 1. 依赖库导入

将alfus.jar导入Android工程

## 2. 权限申请

```xml
<uses-permission android:name="android.permission.ACCESS_SKIN_SERVICE"/>
```

## 3. 初始化SkinManager

通过Alfus.connect()绑定换肤service，绑定成功后即可获取SkinManager。

```java
private SkinManagerHelper(Context context) {
    Log.d(TAG, "SkinManagerHelper");
    mContext = context;
    mAlfus = Alfus.createAlfus(context, new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            Log.d(TAG, "onServiceConnected");
            try {
                mSkinManager = (SkinManager) mAlfus.getAlfusManager(Alfus.SKIN_MANAGER);
                Log.d(TAG, "onServiceConnected mSkinManager = " + mSkinManager);
            } catch (AlfusNotConnectedException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            Log.d(TAG, "onServiceDisconnected");
            mSkinManager = null;
            if (mAlfus != null) {
                mAlfus.connect();
            }
        }
    });
    mAlfus.connect();
}
```

## 4. 调用换肤接口

调用SkinManager的enableSkin(skinId, delayPackage)接口完成换肤操作。

skinId需传入`preset_skin_config.xm`中的主题包ID（参考第三章），此ID生成规则为"com.neusoft.skin."+"主题包文件夹名"。

```java
/**
 * 
 * @param skinId 主题包ID，例：com.neusoft.skin.Blue
 * @param delayPackage 当前包名，例：getPackageName()
 */
public void enableSkin(String skinId, String delayPackage) {
    if (mSkinManager == null) {
        return;
    }

    try {
        mSkinManager.enableSkin(skinId, delayPackage);
    } catch (RemoteException e) {
        e.printStackTrace();
    }
}
```



# 三、主题配置

需要创建更多的主题样式时，可参照下述步骤。

## 1. 创建主题目录

进入Android源码工程目录`AndroidPF/apps/LINUX/android/vendor/naaivi/external/skins/`

创建文件夹作为主题目录如Blue、Green等，将app的皮肤包（皮肤包的制作请参考第二章）工程放置其中，目录结构如下所示：
`└── skins
    ├── Android.mk
    ├── pack.sh
    ├── Golden
    ├── Green
    ├── Blue
    │   └── Audio
    │       ├── AndroidMainfest.xml
    │       ├── Android.mk
    │       └── res
    │           └── values
    │           └── drawable-mdpi
    │   └── Home
    │   └── Radio
    │   └── ... ...
    └── ... ...`

## 2. 换肤原理说明

1. 当skins文件夹执行编译命令时，pack.sh会自动扫描skins目录，并将全部皮肤包信息写入皮肤清单`preset_skin_config.xml`文件中，该文件会最终会push到车机`/system/product/etc/skins/`下供SkinManagerService使用。
2. app端调用换肤接口时（参考第三章），SkinManagerService会对`preset_skin_config.xml`清单文件进行解析。然后依次调用OMS的setEnabledExclusive接口使相应主题的全部app皮肤包生效，实现换肤效果。

`preset_skin_config.xml`内容如下：

```xml
<skins>
    ... ...
	<skin>
		<id>com.neusoft.skin.Blue</id>
		<name>Blue</name>
		<packages>
			<package>com.neusoft.audio.skin.blue</package>
			<package>com.neusoft.video.main.skin.blue</package>
			<package>com.neusoft.home.skin.blue</package>
			<package>com.neusoft.radio.skin.blue</package>
		</packages>
		<preview>
			<preview_path>product/etc/skins/Blue/preview/home_big.png</preview_path>
			<preview_path>product/etc/skins/Blue/preview/home_big_01.png</preview_path>
			<preview_path>product/etc/skins/Blue/preview/home_big_02.png</preview_path>
		</preview>
		<wallpaper>
			<wallpaper_path>product/etc/skins/Blue/wallpaper/bg.png</wallpaper_path>
		</wallpaper>
		<price>0</price>
		<company>Neusoft</company>
		<url>http://www.neusoft.com</url>
	</skin>
    ... ...
</skins>
```

有关OMS内容，可参考Google文档：https://source.android.google.cn/devices/architecture/rros#setting-up-the-manifest
