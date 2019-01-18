using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using CoAP;

public class CoapMessage : MonoBehaviour {

    public string room;
    public string resource;

    public bool state;

    //private string uri = "172.20.10.7";
    //private string uri = "192.168.1.47";
    //private string uri = "172.16.13.56";
    private string uri = "192.168.0.37";
    private string port = "3005";

    public void Start()
    {
        Request request1 = new Request(Method.POST);
        request1.URI = new Uri("coap://" + uri + ":" + port + "/" + room);
        request1.SetPayload("{\"object\": '" + resource + "', 'state': '" + state + "'}");
        request1.Send();
        // wait for one response
        //Response response1 = request1.WaitForResponse();
        state = !state;
        Debug.Log("Message sent");
    }

    public void Get()
    {
        Request request = new Request(Method.GET);
        request.URI = new Uri("coap://" + uri + ":" + port + "/" + room);
        request.Send();
        // wait for one response
        //Response response = request.WaitForResponse();
    }

    public void Post()
    {
        Request request = new Request(Method.POST);
        request.URI = new Uri("coap://" + uri + ":" + port + "/" + room);
        request.SetPayload("{'object':'" + resource + "', 'state': '" + state + "'}");
        request.Send();
        // wait for one response
        //Response response = request.WaitForResponse();
        state = !state;
    }

    public void Put()
    {

        Request request = new Request(Method.PUT);
        request.URI = new Uri("coap://" + uri + ":" + port + "/" + room);
        request.SetPayload("{'object':'" + resource + "', 'state': '" + state + "'}");
        request.Send();
        // wait for one response
        //Response response = request.WaitForResponse();
    }
}
