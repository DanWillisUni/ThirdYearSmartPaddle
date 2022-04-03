package com.example.kayakdatacollection;

import static android.os.Environment.getExternalStorageDirectory;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.provider.ContactsContract;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.DecimalFormat;
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

    private static final int STORAGE_PERMISSION_CODE = 100;
    private static final DecimalFormat df = new DecimalFormat("0.0000000000");

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
        checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,STORAGE_PERMISSION_CODE);
        fileName = "";
        dir = new File(Environment.getExternalStorageDirectory(),"KayakData");
        System.out.println(dir.getPath());
        if(!dir.exists()){
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
                    checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,STORAGE_PERMISSION_CODE);
                    sleep(3000);
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
                    String line = System.currentTimeMillis() + "," + df.format(tx) + "," + df.format(ty) + "," + df.format(tz);
                    writeToFile(fileName + "_accel.txt",line);
                }
            }
        });
        gyroscope.setListener(new Gyroscope.Listener() {
            @Override
            public void onRotation(float rx, float ry, float rz) {
                if(isInSession && fileName != ""){
                    String line = System.currentTimeMillis() + "," + df.format(rx) + "," + df.format(ry) + "," + df.format(rz);
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

    public void checkPermission(String permission, int requestCode)  {
        if (ContextCompat.checkSelfPermission(MainActivity.this, permission) == PackageManager.PERMISSION_DENIED) {
            // Requesting the permission
            ActivityCompat.requestPermissions(MainActivity.this, new String[] { permission }, requestCode);
        }
        else {
            Toast.makeText(MainActivity.this, "Permission already granted", Toast.LENGTH_SHORT).show();
        }
    }

    private boolean writeToFile(String filename, String content){
        try {
            File f = new File(dir,filename);
            FileWriter writer = new FileWriter(f,true);
            writer.append(content + "\r\n");
            writer.flush();
            writer.close();
            //System.out.println(f.getAbsolutePath() + " appended " + content);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    private void sleep(int ms){
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}