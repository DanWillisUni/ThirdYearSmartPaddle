package com.example.kayakdatacollection;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity{
    private Accelerometer accelerometer;
    private Gyroscope gyroscope;
    private Rotation rotationVector;
    private boolean isInSession = false;

    private String currentSessionName = "";
    private String fileName = "";
    private File writeDir;
    private String IMEI;
    private List<String> currentAccel;
    private List<String> currentGyro;
    private List<String> currentRota;
    private long currentSessionStartTime;

    private static final int STORAGE_PERMISSION_CODE = 100;
    private static final int STATE_PERMISSION_CODE = 101;
    private static final DecimalFormat df = new DecimalFormat("0.0000000000");
    private static final int IGNORE_TIME = 3000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        isInSession = false;
        currentSessionName = "";

        //device ID
        IMEI = getUniqueIMEIId();

        //file setup
        checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,STORAGE_PERMISSION_CODE);
        fileName = "";
        writeDir = new File(Environment.getExternalStorageDirectory(),"KayakData");
        System.out.println(writeDir.getPath());
        if(!writeDir.exists()){
            writeDir.mkdirs();
            System.out.println("Making new Dir");
        }

        //setup dropdown
        Spinner dropdown = findViewById(R.id.activity_spinner);
        String[] items = new String[]{"Perfect", "Over-Reaching", "Not-Upright", "Stroke-Too-Wide", "Blade-Angle-Wrong","Test"};
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
        final ImageButton button = findViewById(R.id.StopStartButton);
        button.setBackgroundColor(Color.GREEN);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(isInSession){
                    long stopTime = System.currentTimeMillis();
                    onPause();
                    isInSession = false;
                    System.out.println("Stop: " + System.currentTimeMillis());
                    button.setImageResource(R.drawable.ic_baseline_play_arrow_24);
                    button.setBackgroundColor(Color.GREEN);
                    //post processing the files
                    List<String> accelToPublish = new ArrayList<String>();
                    for (String line:currentAccel) {
                        if(Long.parseLong(line.split(",")[0]) < stopTime- IGNORE_TIME && Long.parseLong(line.split(",")[0]) > currentSessionStartTime + IGNORE_TIME){
                            accelToPublish.add(line);
                        }
                    }
                    List<String> gyroToPublish = new ArrayList<String>();
                    for (String line:currentGyro) {
                        if(Long.parseLong(line.split(",")[0]) < stopTime- IGNORE_TIME && Long.parseLong(line.split(",")[0]) > currentSessionStartTime + IGNORE_TIME){
                            gyroToPublish.add(line);
                        }
                    }
                    List<String> rotaToPublish = new ArrayList<String>();
                    for (String line:currentRota) {
                        if(Long.parseLong(line.split(",")[0]) < stopTime- IGNORE_TIME && Long.parseLong(line.split(",")[0]) > currentSessionStartTime + IGNORE_TIME){
                            rotaToPublish.add(line);
                        }
                    }
                    writeToFile(fileName + "_accel.txt",accelToPublish);
                    writeToFile(fileName + "_gyro.txt",gyroToPublish);
                    writeToFile(fileName + "_rota.txt",rotaToPublish);
                    Toast.makeText(MainActivity.this, fileName, Toast.LENGTH_SHORT).show();
                    fileName = "";
                }else{
                    currentSessionStartTime = System.currentTimeMillis();
                    System.out.println("Start: " + currentSessionStartTime);
                    fileName = MainActivity.this.IMEI + "_" + currentSessionStartTime + "_" + currentSessionName;
                    //checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,STORAGE_PERMISSION_CODE);
                    currentAccel = new ArrayList<String>();
                    currentGyro = new ArrayList<String>();
                    currentRota = new ArrayList<String>();
                    isInSession = true;
                    button.setImageResource(R.drawable.ic_baseline_stop_24);
                    button.setBackgroundColor(Color.RED);
                    onResume();
                }
            }
        });

        ImageButton btn = (ImageButton) findViewById(R.id.ToInfoButton);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, DisplayFeedback.class));
            }
        });

        //setup sensors
        accelerometer = new Accelerometer(this);
        gyroscope = new Gyroscope(this);
        rotationVector = new Rotation(this);
        accelerometer.setListener(new Accelerometer.Listener() {
            @Override
            public void onTranslation(float tx, float ty, float tz) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + df.format(tx) + "," + df.format(ty) + "," + df.format(tz);
                    currentAccel.add(line);
                }
            }
        });
        gyroscope.setListener(new Gyroscope.Listener() {
            @Override
            public void onRotation(float rx, float ry, float rz) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + df.format(rx) + "," + df.format(ry) + "," + df.format(rz);
                    currentGyro.add(line);
                }
            }
        });
        rotationVector.setListener(new Rotation.Listener() {
            @Override
            public void onRotation(float tx,float ty,float tz,float v3,float v4) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + df.format(tx) + "," + df.format(ty) + "," + df.format(tz)+ "," + df.format(v3)+ "," + df.format(v4);
                    currentRota.add(line);
                }
            }
        });
    }

    @Override
    protected void onResume(){
        super.onResume();

        accelerometer.register();
        gyroscope.register();
        rotationVector.register();
    }
    @Override
    protected void onPause() {
        super.onPause();

        accelerometer.unregister();
        gyroscope.unregister();
        rotationVector.unregister();
    }

    public void checkPermission(String permission, int requestCode)  {
        if (ContextCompat.checkSelfPermission(MainActivity.this, permission) == PackageManager.PERMISSION_DENIED) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[] { permission }, requestCode);// Requesting the permission
        } else {
            Toast.makeText(MainActivity.this, "Permission for " + permission + " already granted", Toast.LENGTH_SHORT).show();
        }
    }

    private boolean writeToFile(String filename, List<String> content){
        try {
            if(!content.isEmpty()){
                File f = new File(writeDir,filename);
                FileWriter writer = new FileWriter(f);
                for (String line:content) {
                    writer.append(line + "\r\n");
                }
                writer.flush();
                writer.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public String getUniqueIMEIId() {
        try {
            checkPermission(Manifest.permission.READ_PHONE_STATE,STATE_PERMISSION_CODE);
            TelephonyManager telephonyManager = (TelephonyManager) this.getSystemService(Context.TELEPHONY_SERVICE);
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {
                return "";
            }
            @SuppressLint("MissingPermission") String imei = telephonyManager.getDeviceId();
            Log.e("imei", "=" + imei);
            if (imei != null && !imei.isEmpty()) {
                return imei;
            } else {
                return android.os.Build.SERIAL;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "not_found";
    }
}