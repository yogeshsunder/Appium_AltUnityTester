package ro.altom.altunitytesterexample;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.android.AndroidDriver;

import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.annotations.Test;

import com.google.gson.Gson;

import ro.altom.altunitytester.AltUnityDriver;
import ro.altom.altunitytester.AltUnityDriver.By;
import ro.altom.altunitytester.AltUnityObject;

import static org.testng.Assert.assertEquals;
import static org.testng.Assert.assertNotNull;
import static org.testng.Assert.assertTrue;

import java.io.File;
import java.net.URL;
import java.util.concurrent.TimeUnit;

public class CheckAltUnityTesterConnectivity {

	public static AndroidDriver<MobileElement> appiumDriver;
	public static AltUnityDriver altUnityDriver;
    
	@SuppressWarnings("deprecation")
	@Test
    public static void main() throws Exception {
        //AltUnityDriver.setupPortForwarding("android", "", 13000, 13000);
        File app = new File("E:\\build (1).apk");
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability(CapabilityType.BROWSER_NAME, "");
        capabilities.setCapability("deviceName", "Pixel 2 API 28");
        capabilities.setCapability("platformName", "Android");
        capabilities.setCapability("app", app.getAbsolutePath());
        appiumDriver = new AndroidDriver<MobileElement>(new URL("http://127.0.0.1:4723/wd/hub"), capabilities);
        appiumDriver.manage().timeouts().implicitlyWait(80, TimeUnit.SECONDS);
        
        Thread.sleep(5000);
       
       AltUnityDriver.setupPortForwarding("android","", 13000, 13000);
       
       Thread.sleep(25000);
       //Thread.sleep(5000);
       
        altUnityDriver = new AltUnityDriver("127.0.0.1", 13000, ";", "&", true);
        
        Thread.sleep(5000);
        
        System.out.println("App Forwarded to AltUnity Tester.");
        
        Thread.sleep(2000);
        
        String currentScene = altUnityDriver.getCurrentScene();
        
        System.out.println(currentScene);
        
        altUnityDriver.loadScene("Online Controller Scene");
        
        altUnityDriver.findElement("CREATE ACCOUNT").clickEvent();

        
        //altUnityDriver.findElement("IMPORT").clickEvent();
        
        //altUnityDriver.findElement("IMPORT").clickEvent();
        
        //String name = "IMPORT";
        //AltUnityObject altElement = altUnityDriver.findObject(AltUnityDriver.By.NAME,name);
        
        //System.out.println(altElement);
        //assertNotNull(altElement);
        //assertEquals(name, altElement.name);
        
    }
}
