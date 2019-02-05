package com.example.shashankavs.iot;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.text.util.Linkify;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.InputStream;

public class YesActivity extends MainActivity {

    public FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReferenceFromUrl("gs://iotfirebaseproject-55895.appspot.com/").child("yes.txt");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yes);
        // Get the Intent that started this activity and extract the string
        Intent yesintent = getIntent();
        // Capture the layout's TextView and set the string as its text
        TextView textView = findViewById(R.id.textView_yes);
        TextView noteView = (TextView) findViewById(R.id.textView);
        Linkify.addLinks(noteView, Linkify.ALL);

        InputStream stream = getResources().openRawResource(R.raw.yes);
        UploadTask uploadTask = storageRef.putStream(stream);
        uploadTask.addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception exception) {
                exception.printStackTrace();
                //dismissProgressDialog();
                Toast.makeText(YesActivity.this, "Upload Failed!", Toast.LENGTH_SHORT).show();
            }
        }).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                // dismissProgressDialog();
                Toast.makeText(YesActivity.this, "Uploaded!", Toast.LENGTH_SHORT).show();
            }
        });
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                deleteText();
            }
        }, 25000);
    }

    public void deleteText(){
        storageRef.delete().addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void aVoid) {
                Toast.makeText(YesActivity.this, "Deleted!", Toast.LENGTH_SHORT).show();
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception exception) {
                Toast.makeText(YesActivity.this, "Delete failed!", Toast.LENGTH_SHORT).show();
            }
        });
    }
}

