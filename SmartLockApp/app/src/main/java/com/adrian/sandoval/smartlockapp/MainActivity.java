package com.adrian.sandoval.smartlockapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.RemoteException;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.TimeoutError;
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

    private ImageView logout =null;

    String sending_url = null;

    RequestQueue queue = null;

    Boolean mInZone, REEQUEST_COMPLETE = null;

    Handler handler =null;

    Integer WAIT_PERIOD = null;
    Integer DELAY = null;

    private static DecimalFormat decimalFormat = new DecimalFormat("0.00");

    private SeekBar seekBar = null;

    private Switch aSwitch = null;

    private static int SENSINTIVITY;
    private static int SENSINTIVITY_VALUE;
    private static int mLOW = -47;
    private static int mMEDIUM = -65;
    private static int mHIGH = -80;

    private String username = null;
    private String PIN = null;
    private String IP = null;

    private Boolean LOGGEDOUT =null;

    private String online_url = "http://adsanvar.pythonanywhere.com/";
    //private String online_url = "http://192.168.1.74:5000/";


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

        username = getIntent().getStringExtra("Username");

        mbutton = this.findViewById(R.id.btnUnlock);
        dis = this.findViewById(R.id.distance_id);
        mUrl = this.findViewById(R.id.url_id);
        mresponse = this.findViewById(R.id.response_id);
        inzonetxt = this.findViewById(R.id.inzone_id);
        seekBar = this.findViewById(R.id.seekBar);
        txtSensativity = this.findViewById(R.id.txtSensativity);
        aSwitch = this.findViewById(R.id.info_switch);
        logout = this.findViewById(R.id.iv_logout);

        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), Home.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK|Intent.FLAG_ACTIVITY_NEW_TASK);
                LOGGEDOUT = true;
                getApplicationContext().startActivity(intent);
                finish();
            }
        });

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
        LOGGEDOUT = false;
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
                    setSensitivity(getApplicationContext(), Integer.toString(progress));
                }
                else if(progress == 1)
                {
                    txtSensativity.setText("Sensitivity:" + "\n" + "Medium");
                    SENSINTIVITY = mMEDIUM;
                    setSensitivity(getApplicationContext(), Integer.toString(progress));
                }
                else
                {
                    txtSensativity.setText("Sensitivity:"+ "\n" + "High");
                    SENSINTIVITY = mHIGH;
                    setSensitivity(getApplicationContext(), Integer.toString(progress));
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

        DELAY = 2000;

        //get User Information
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
               getUserInformation(getApplicationContext());

            }
        }, DELAY);
        //getUserInformation(this);


    }

//                new AlertDialog.Builder(context)
//            .setTitle("Unable To Acquire User Settings?")
//                        .setMessage("Would Like To Retry?")
//
//    // Specifying a listener allows you to take an action before dismissing the dialog.
//    // The dialog is automatically dismissed when a dialog button is clicked.
//                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
//        public void onClick(DialogInterface dialog, int which) {
//            // Continue with delete operation
//            getUserInformation(context);
//        }
//    })
//
//            // A null listener allows the button to dismiss the dialog and take no further action.
//            .setNegativeButton(android.R.string.no, null)
//                        .setIcon(android.R.drawable.ic_dialog_alert)
//                        .show();

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
                                //mresponse.setText("Response is: "+ response);
                                resp = response;
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        if(error instanceof TimeoutError){
                            //do nothing
                        }else
                        {
                            mresponse.setText("Response Status:\n" + error.toString());
                        }
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
                    mresponse.setText("Response Status:\nTask Completed");
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
//        mBeaconManager.unbind(this);
        mBeaconManager = BeaconManager.getInstanceForApplication(this.getApplicationContext());
        // Detect the URL frame:
        mBeaconManager.getBeaconParsers().add(new BeaconParser().
                setBeaconLayout(BeaconParser.EDDYSTONE_URL_LAYOUT));
        mBeaconManager.bind(this);
    }

    @Override
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
        if(!LOGGEDOUT)
        {
            for (Beacon beacon: beacons) {
                if (beacon.getServiceUuid() == 0xfeaa && beacon.getBeaconTypeCode() == 0x10) {
                    // This is a Eddystone-URL frame
                    String url = UrlBeaconUrlCompressor.uncompress(beacon.getId1().toByteArray());
                    Log.d(TAG, "I see a beacon transmitting a url: " + url +
                            " approximately " + beacon.getDistance() + " meters away."+" Rssi: " +beacon.getRssi());
                    dis.setText("Distance: " + decimalFormat.format(beacon.getDistance()) +"m" +"\nRSSI: "+ beacon.getRssi());
                    if (url.equals("http://"+IP))
                    {
                        sending_url = url +":5000/mobileUnlock/"+PIN;
                        mUrl.setText("Advertising:\n" +url);
                        //setmInZone(beacon.getDistance());
                        setmInZone(beacon.getRssi());
                        passiveEntry();
                    }


                }
            }
        }

    }

    @Override
    public void onPause() {
        super.onPause();
        mBeaconManager.unbind(this);
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        mBeaconManager.unbind(this);
    }

    /**
     * Set Sensitivity of the User
     * @param context
     * @param sensitivity
     */
    protected void setSensitivity(final Context context, String sensitivity)
    {
        final String info = online_url + "setSensitivity/"+username+"/"+sensitivity;
        StringRequest stringRequest = new StringRequest(Request.Method.GET, info, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

                Toast.makeText(context, "Update: "+response, Toast.LENGTH_LONG).show();


            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                if(error instanceof TimeoutError){
                    //do nothing
                }else
                {   Log.d("RESPONSE", error.toString());
                    Toast.makeText(context, "Unable To Update User Info", Toast.LENGTH_LONG).show();
                }

            }
        });

        queue.add(stringRequest);

    }
    /**
     * Gets information for authentication
     * @param context
     */
    protected void getUserInformation(final Context context)
    {
        final String info = online_url + "getUserInfo/"+username;
        StringRequest stringRequest = new StringRequest(Request.Method.GET, info, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

                //Toast.makeText(context, response, Toast.LENGTH_LONG).show();
                String[] tokens = response.split(",");
                PIN = tokens[0];
                IP = tokens[1];
                SENSINTIVITY_VALUE = Integer.parseInt(tokens[2]);
                seekBar.setProgress(SENSINTIVITY_VALUE);


            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                Log.d("RESPONSE", error.toString());
                Toast.makeText(context, "Unable To Acquire User Info", Toast.LENGTH_LONG).show();
            }
        });

        queue.add(stringRequest);

    }


}
