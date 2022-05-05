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

        ImageView correction = (ImageView) findViewById(R.id.correctionImage);
        String biggestError = calculateBiggestError();
        int correctionImage = getCorrectionImage(biggestError);
        correction.setImageResource(correctionImage);

        TextView textView = findViewById(R.id.textView);
        textView.setText(getRankUpSentance(perfectPercent) + biggestError);
    }

    private double calculatePerfectPercent(){
        int total = 0;
        for (int i:feedbackArray) {
            total+= i;
        }
        return (double)(feedbackArray[0]/total);
    }

    private int getImageName(double perfectPercent){
        if(perfectPercent < 20){
            return R.drawable.Tadpole;
        } else if(perfectPercent < 40){
            return R.drawable.Salmon;
        } else if(perfectPercent < 60){
            return R.drawable.Squid;
        } else if(perfectPercent < 80){
            return R.drawable.Dolphin;
        }
        return R.drawable.Shark;
    }

    private String getRankUpSentance(double perfectPercent){
        if(perfectPercent < 20){
            return "Like a Tadpole your journeys only just beginning \n" +
                    "To become a salmon focus on ";
        } else if(perfectPercent < 40){
            return "Well done!  You are a salmon! \n" +
                    "To become a squid, focus on ";
        } else if(perfectPercent < 60){
            return "Congratulations, you are a Salmon!\n" +
                    " To become a Dolphin, focus on ";
        } else if(perfectPercent < 80){
            return "Great Job, you are a Dolphin! \n" +
                    "To become a Shark focus on ";
        }
        String r = "Fantastic! You are a shark in the water!";
        if (perfectPercent < 100){
            r += "\nTo improve even more focus on ";
        }
        return r;
    }

    private String calculateBiggestError(){
        int max = 0;
        int maxI = 0;
        for (int i = 1; i < feedbackArray.length; i++) {
            if(feedbackArray[i]>max){
                max = feedbackArray[i];
                maxI = i;
            }
        }
        return feedbackImageNames[maxI-1];
    }

    private int getCorrectionImage(String errorName){
        if (errorName == "OverReaching"){
            return R.drawable.OverReach;
        } else if (errorName == "NotUpright"){
            return R.drawable.Salmon;//change
        } else if (errorName == "StrokeTooWide"){
            return R.drawable.TooWide;
        } else if (errorName == "BladeAngleWrong"){
            return R.drawable.BladeAngle;
        }
        return R.drawable.Perfect;
    }
}
