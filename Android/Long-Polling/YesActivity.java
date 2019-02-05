package com.example.shashankavs.npiot;

import android.Manifest;
import android.annotation.TargetApi;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.net.Socket;

public class YesActivity extends MainActivity {

    protected boolean shouldAskPermissions() {
        return (Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP_MR1);
    }

    @TargetApi(23)
    protected void askPermissions() {
        String[] permissions = {
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.WRITE_EXTERNAL_STORAGE"
        };
        int requestCode = 200;
        requestPermissions(permissions, requestCode);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yes);
        // Get the Intent that started this activity and extract the string
        Intent yesintent = getIntent();
        // Capture the layout's TextView and set the string as its text
        TextView textView = findViewById(R.id.textView_yes);

        File file = new File ("/storage/emulated/0/yes.txt");

        try {
            Socket s = new Socket("52.90.46.91", 9999);
            Toast.makeText(YesActivity.this, "Uploaded!",
                    Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Log.e("Error Message", e.getMessage());
        }
    }
}