package com.example.kayakdatacollection;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class MainActivity extends AppCompatActivity {

    private Accelerometer accelerometer;
    private Gyroscope gyroscope;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //setup dropdown
        Spinner dropdown = findViewById(R.id.activity_spinner);
        String[] items = new String[]{"Excellent", "Good", "Bad"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(adapter);

        //setup button
        final boolean[] isInSession = {false};
        final Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(isInSession[0]){
                    isInSession[0] = false;
                    button.setText("Start");
                    getWindow().getDecorView().setBackgroundColor(Color.WHITE);
                    onPause();
                }
                else{
                    isInSession[0] = true;
                    button.setText("Stop");
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
                if(tx > 1.0f){
                    getWindow().getDecorView().setBackgroundColor(Color.RED);
                }
                else if(tx < -1.0f){
                    getWindow().getDecorView().setBackgroundColor(Color.BLUE);
                }
            }
        });
        gyroscope.setListener(new Gyroscope.Listener() {
            @Override
            public void onRotation(float rx, float ry, float rz) {
                if(ry > 1.0f){
                    getWindow().getDecorView().setBackgroundColor(Color.GREEN);
                }
                else if(ry< -1.0f){
                    getWindow().getDecorView().setBackgroundColor(Color.YELLOW);
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
}