package com.adrian.sandoval.smartlockapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.RemoteException;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.altbeacon.beacon.Beacon;
import org.altbeacon.beacon.BeaconConsumer;
import org.altbeacon.beacon.BeaconManager;
import org.altbeacon.beacon.BeaconParser;
import org.altbeacon.beacon.RangeNotifier;
import org.altbeacon.beacon.Region;
import org.altbeacon.beacon.utils.UrlBeaconUrlCompressor;

import java.util.Collection;

public class Home extends AppCompatActivity {

private Button btnLogin;
private EditText txtUsername, txtPassword;
private ImageView logo;
private Context context;
private RequestQueue queue = null;
private Handler handler =null;
private Integer WAIT_PERIOD = null;
private String sending_url = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        btnLogin = findViewById(R.id.btnLogin);
        txtUsername = findViewById(R.id.txtUsername);
        txtPassword = findViewById(R.id.txtPassword);
        logo = findViewById(R.id.logo);
        context = this;

        sending_url = '192.168.1.65:5000/'


        Animation anim = AnimationUtils.loadAnimation(this, R.anim.fadein);
        logo.startAnimation(anim);
        txtUsername.startAnimation(anim);
        txtPassword.startAnimation(anim);
        btnLogin.startAnimation(anim);
        txtUsername.requestFocus();

        queue = Volley.newRequestQueue(this);
        handler = new Handler();
        WAIT_PERIOD = 13*1000;

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                final Animation animation = AnimationUtils.loadAnimation(v.getContext(), R.anim.blink_anim);

                if ((userNameText.getText().toString().equals(manager)) && (passwordText.getText().toString().equals(password))) {
                    accountType = true;
                    Intent intent = new Intent(v.getContext(), MainActivity.class);
                    intent.putExtra("AccountType", accountType);
                    intent.putExtra("userName", manager);
                    intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                    v.getContext().startActivity(intent);
                    overridePendingTransition(R.anim.fadein, R.anim.fadeout);

                } else if ((userNameText.getText().toString().equals(employe)) && (passwordText.getText().toString().equals(password2))) {
                    accountType = false;

                    Intent intent = new Intent(v.getContext(), MainActivity.class);
                    intent.putExtra("AccountType", accountType);
                    intent.putExtra("userName", employe);
                    intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                    v.getContext().startActivity(intent);
                    overridePendingTransition(R.anim.fadein, R.anim.fadeout);


                } else {

                    Toast.makeText(v.getContext(), "Invalid Credential", Toast.LENGTH_LONG).show();
                    loginButton.setText("Error");
                    loginButton.setTextColor(getResources().getColor(R.color.white));
                    loginButton.startAnimation(animation);
                    loginButton.setBackground(getResources().getDrawable(R.drawable.login_failed_button));


                }

                v.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        btnLogin.setBackground(getResources().getDrawable(R.drawable.login_button));
                        btnLogin.setText("Login");
                        btnLogin.setTextColor(getResources().getColor(R.color.white));
                        btnLogin.clearAnimation();
                        animation.cancel();

                    }
                }, 1000);

            }
        });

    }

    public void login()
    {
        new Home.SendRequest().execute(sending_url);

    }

    protected class SendRequest extends AsyncTask<String, Integer, String> {
        String resp = null;

        protected  String doInBackground(final String... urls)
        {

            for(int i =0; i < urls.length; i++)
            {
                StringRequest stringRequest = new StringRequest(Request.Method.POST, urls[i],
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                                //mresponse.setText("Response is: "+ response);
                                resp = response;
                                Toast.makeText(context, "Response: " + resp.toString(), Toast.LENGTH_SHORT).show();
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(context, "Response: " + resp.toString(), Toast.LENGTH_SHORT).show();
                        //mresponse.setText("That didn't work!: " + error.toString());
                        Log.d("Connection", error.toString());
                    }
                });

                queue.add(stringRequest);
            }

            return resp;

        }


        //When post has executed
        protected  void onPostExecute(final String result)
        {
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(context, result, Toast.LENGTH_SHORT).show();

                }
            }, WAIT_PERIOD);



        }
    }


}

