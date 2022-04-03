package com.example.kayakdatacollection;

import static android.os.Environment.getExternalStorageDirectory;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity{
    private Accelerometer accelerometer;
    private Gyroscope gyroscope;
    private boolean isInSession = false;
    private String currentSessionName = "";
    private String fileName = "";
    private File dir;
    private String IMEI;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        isInSession = false;
        currentSessionName = "";

        //device ID
        /*TelephonyManager tm=(TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE);
        int readIMEI= ContextCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE);
        if(IMEI == null) {
            if (readIMEI == PackageManager.PERMISSION_GRANTED) {
                IMEI = android.provider.Settings.Secure.getString(this.getContentResolver(), android.provider.Settings.Secure.ANDROID_ID);
            }
        }*/

        //file setup
        fileName = "";
        dir = new File("storage/self/primary","KayakData");
        System.out.println(dir.getPath());
        if(!dir.isDirectory()){
            dir.mkdirs();
            System.out.println("Making new Dir");
        }

        //setup dropdown
        Spinner dropdown = findViewById(R.id.activity_spinner);
        String[] items = new String[]{"Excellent", "Good", "Bad"};
        ArrayAdapter<String> dropdownList = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(dropdownList);
        dropdown.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                currentSessionName = dropdownList.getItem(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
                currentSessionName = "";
            }

        });

        //setup button
        final Button button = findViewById(R.id.button);
        button.setText("Start");
        final TextView t = findViewById(R.id.current_activity);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(isInSession){
                    long stopTime = System.currentTimeMillis();
                    button.setText("Start");
                    isInSession = false;
                    onPause();

                    //post process the files to remove last 3 seconds
                    fileName = "";
                }
                else{
                    button.setText("Stop");
                    fileName = MainActivity.this.IMEI + "_" + System.currentTimeMillis() + "_" + currentSessionName;
                    try {
                        File accelFile = new File(dir,fileName + "_accel.txt");
                        System.out.println(accelFile.getAbsolutePath());
                        accelFile.createNewFile();
                        File gyroFile = new File(dir,fileName + "_gyro.txt");
                        gyroFile.createNewFile();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    try {
                        Thread.sleep(3000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    t.setText(fileName);
                    isInSession = true;
                    onResume();
                }
            }
        });

        //setup sensors
        accelerometer = new Accelerometer(this);
        gyroscope = new Gyroscope(this);
        accelerometer.setListener(new Accelerometer.Listener() {
            @Override
            public void onTranslation(float tx, float ty, float tz) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + tx + "," + ty + "," + tz;
                    writeToFile(fileName + "_accel.txt",line);
                }
            }
        });
        gyroscope.setListener(new Gyroscope.Listener() {
            @Override
            public void onRotation(float rx, float ry, float rz) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + rx + "," + ry + "," + rz;
                    writeToFile(fileName + "_gyro.txt",line);
                }
            }
        });
    }

    @Override
    protected void onResume(){
        super.onResume();

        accelerometer.register();
        gyroscope.register();
    }

    @Override
    protected void onPause() {
        super.onPause();

        accelerometer.unregister();
        gyroscope.unregister();
    }

    private boolean writeToFile(String fileName, String content){
        try {
            File f = new File(dir,fileName);
            FileOutputStream fs = openFileOutput(f.getAbsolutePath(), MODE_APPEND);
            fs.write((content + "\r\n").getBytes());
            fs.close();
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }
}