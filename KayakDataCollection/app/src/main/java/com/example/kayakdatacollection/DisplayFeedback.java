package com.example.kayakdatacollection;

import android.Manifest;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DisplayFeedback extends AppCompatActivity {
    int[] feedbackArray = new int[] {0,10,21,20,0};
    String[] feedbackImageNames = new String[] {"OverReaching","NotUpright","StrokeTooWide","BladeAngleWrong"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.display_feedback);
        Intent intent = getIntent();

        double perfectPercent = calculatePerfectPercent();
        int imageToDisplay = getImageName(perfectPercent);
        ImageView rank = (ImageView) findViewById(R.id.rankImage);
        rank.setImageResource(imageToDisplay);

    }

    private double calculatePerfectPercent(){
        int total = 0;
        for (int i:feedbackArray) {
            total+= i;
        }
        return (double)(feedbackArray[0]/total);
    }

    private int getImageName(double perfectPercent){
        /*if(perfectPercent < 20){

        } else if(perfectPercent < 40){

        } else if(perfectPercent < 60){

        } else if(perfectPercent < 80){

        }*/
        return R.drawable.shark;
    }
}
