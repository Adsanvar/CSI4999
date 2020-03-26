package com.adrian.sandoval.smartlockapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.RemoteException;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;
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

import java.text.DecimalFormat;
import java.util.Collection;

public class MainActivity extends AppCompatActivity implements BeaconConsumer, RangeNotifier {

    private static String TAG = "MyActivity";
    private BeaconManager mBeaconManager;

    //Bluetooth adapter
    private BluetoothAdapter bluetoothAdapter;

    //Request number must be greater than 0
    private final static int REQUEST_ENABLE_BT = 1;

    //button
    Button mbutton = null;

    private TextView dis, mUrl, mresponse, inzonetxt, txtSensativity = null;

    String sending_url = null;

    RequestQueue queue = null;

    Boolean mInZone, REEQUEST_COMPLETE = null;

    Handler handler =null;

    Integer WAIT_PERIOD = null;

    private static DecimalFormat decimalFormat = new DecimalFormat("0.00");

    private SeekBar seekBar = null;

    private Switch aSwitch = null;

    private static int SENSINTIVITY;
    private static int mLOW = -35;
    private static int mMEDIUM = -55;
    private static int mHIGH = -75;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
            Toast.makeText(this, "BLE NOT SUPPORTED", Toast.LENGTH_SHORT).show();
            finish();
        }

        // Bluetooth Manager
        final BluetoothManager bluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        bluetoothAdapter = bluetoothManager.getAdapter();


        //Check to see if bluetooth is turned on, if not an Intent is called to allow to connect to BT
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled())
        {
            try {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);

            } catch (ActivityNotFoundException ex) {
                Log.d("ACTIVITY", ex.getMessage());
            }
        }


        mbutton = this.findViewById(R.id.btnUnlock);
        dis = this.findViewById(R.id.distance_id);
        mUrl = this.findViewById(R.id.url_id);
        mresponse = this.findViewById(R.id.response_id);
        inzonetxt = this.findViewById(R.id.inzone_id);
        seekBar = this.findViewById(R.id.seekBar);
        txtSensativity = this.findViewById(R.id.txtSensativity);
        aSwitch = this.findViewById(R.id.info_switch);

        mbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                Intent intent = new Intent(v.getContext(), Home.class);
//                intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
//                v.getContext().startActivity(intent);
                unlock();
            }
        });

        queue = Volley.newRequestQueue(this);
        handler = new Handler();
        WAIT_PERIOD = 13*1000;
        REEQUEST_COMPLETE = true;
        txtSensativity.setText(txtSensativity.getText().toString() + "\n" + "Low");
        SENSINTIVITY = mLOW;

        /*
            Updates the TextView upon changing the seekBar
         */
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Log.d("SeekBar", Integer.toString(progress));
                if(progress == 0)
                {
                    txtSensativity.setText("Sensitivity:" + "\n" + "Low");
                    SENSINTIVITY = mLOW;
                }
                else if(progress == 1)
                {
                    txtSensativity.setText("Sensitivity:" + "\n" + "Medium");
                    SENSINTIVITY = mMEDIUM;
                }
                else
                {
                    txtSensativity.setText("Sensitivity:"+ "\n" + "High");
                    SENSINTIVITY = mHIGH;
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        /*
            Toggles details
         */
        aSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked) {
                    dis.setVisibility(View.VISIBLE);
                    inzonetxt.setVisibility(View.VISIBLE);
                    mresponse.setVisibility(View.VISIBLE);
                    mUrl.setVisibility(View.VISIBLE);
                }else
                {
                    dis.setVisibility(View.INVISIBLE);
                    inzonetxt.setVisibility(View.INVISIBLE);
                    mresponse.setVisibility(View.INVISIBLE);
                    mUrl.setVisibility(View.INVISIBLE);
                }

            }
        });

    }



    public void unlock()
    {
        new SendRequest().execute(sending_url);

    }

    protected class SendRequest extends AsyncTask<String, Integer,String>{
        String resp = null;

        protected  String doInBackground(final String... urls)
        {
            REEQUEST_COMPLETE = false;

            for(int i =0; i < urls.length; i++)
            {
                StringRequest stringRequest = new StringRequest(Request.Method.POST, urls[i],
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                                //mresponse.setText("Response is: "+ response);
                                resp = response;
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        mresponse.setText("That didn't work!: " + error.toString());
                        Log.d("Connection", error.toString());
                        Log.d("Connection", resp);
                    }
                });

                queue.add(stringRequest);
            }

            return resp;

        }

        protected  void onPostExecute(String result)
        {
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    mresponse.setText(mresponse.getText() + "\nTask Completed");
                    REEQUEST_COMPLETE = true;

                }
            }, WAIT_PERIOD);



        }
    }

    protected void passiveEntry()
    {
        inzonetxt.setText("In Zone?\n" + mInZone);
        if(REEQUEST_COMPLETE == true)
        {
            if(mInZone == true)
            {
                new SendRequest().execute(sending_url);

            }
        }

    }


    private void setmInZone(double dis)
    {

        if(SENSINTIVITY == mLOW)
        {
            Log.d("mLOW", Integer.toString(mLOW));
            if(dis > mLOW)
            {
                Log.d("condition", Double.toString(dis));
                mInZone = true;
            }
            else mInZone = false;
        }
        else if(SENSINTIVITY == mMEDIUM)
        {
            Log.d("mMEDIUM", Integer.toString(mMEDIUM));
            if(dis > mMEDIUM)
            {
                mInZone = true;
            }
            else mInZone = false;
        }
        else {
            Log.d("mHIGH", Integer.toString(mHIGH));
            if(dis > mHIGH)
            {
                mInZone = true;
            }
            else mInZone = false;
        }

//        if(dis > 3.5)
//        {
//            mInZone = true;
//        }
//        else mInZone = false;
    }


    @Override
    public void onResume() {
        super.onResume();
        mBeaconManager = BeaconManager.getInstanceForApplication(this.getApplicationContext());
        // Detect the URL frame:
        mBeaconManager.getBeaconParsers().add(new BeaconParser().
                setBeaconLayout(BeaconParser.EDDYSTONE_URL_LAYOUT));
        mBeaconManager.bind(this);
    }

    public void onBeaconServiceConnect() {
        Region region = new Region("all-beacons-region", null, null, null);
        try {
            mBeaconManager.startRangingBeaconsInRegion(region);
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        mBeaconManager.setRangeNotifier(this);
    }

    @Override
    public void didRangeBeaconsInRegion(Collection<Beacon> beacons, Region region) {
        for (Beacon beacon: beacons) {
            if (beacon.getServiceUuid() == 0xfeaa && beacon.getBeaconTypeCode() == 0x10) {
                // This is a Eddystone-URL frame
                String url = UrlBeaconUrlCompressor.uncompress(beacon.getId1().toByteArray());
                sending_url = url +":5000/mobileUnlock/0";
                Log.d(TAG, "I see a beacon transmitting a url: " + url +
                        " approximately " + beacon.getDistance() + " meters away."+" Rssi: " +beacon.getRssi());
                dis.setText("Distance: " + decimalFormat.format(beacon.getDistance()) +"m" +"\nRSSI: "+ beacon.getRssi());
                mUrl.setText("Advertising:\n" +url);
                //setmInZone(beacon.getDistance());
                setmInZone(beacon.getRssi());
                passiveEntry();

            }
        }
    }


    @Override
    public void onPause() {
        super.onPause();
        Log.d("onPause", "True");
        mBeaconManager.unbind(this);
    }
    
}
