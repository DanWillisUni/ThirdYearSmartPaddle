package com.example.kayakdatacollection;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

public class Rotation {
    public interface Listener{
        void onRotation(float tx,float ty,float tz,float v3,float v4);
    }

    private Rotation.Listener listener;
    public void setListener(Rotation.Listener l){
        listener = l;
    }

    private SensorManager sensorManager;
    private Sensor sensor;
    private SensorEventListener sensorEventListener;

    Rotation(Context context){
        sensorManager = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
        sensorEventListener = new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {
                if(listener != null){
                    listener.onRotation(sensorEvent.values[0],sensorEvent.values[1],sensorEvent.values[2],sensorEvent.values[3],sensorEvent.values[4]);
                }
            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {
                //nothing to do here
            }
        };
    }

    public void register(){
        sensorManager.registerListener(sensorEventListener,sensor,SensorManager.SENSOR_DELAY_NORMAL);
    }
    public void unregister(){
        sensorManager.unregisterListener(sensorEventListener);
    }

}
