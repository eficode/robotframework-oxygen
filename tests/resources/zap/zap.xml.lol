<?xml version="1.0"?><OWASPZAPReport version="2.7.0" generated="Tue, 7 Aug 2018 13:17:56">
<site name="http://192.168.50.56:7272" host="192.168.50.56" port="7272" ssl="false"><alerts></alerts></site><site name="http://localhost:7272" host="localhost" port="7272" ssl="false"><alerts><alertitem>
  <pluginid>10012</pluginid>
  <alert>Password Autocomplete in Browser</alert>
  <name>Password Autocomplete in Browser</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;The AUTOCOMPLETE attribute is not disabled on an HTML FORM/INPUT element containing password type input.  Passwords may be stored in browsers and retrieved.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://localhost:7272/</uri>
  <method>GET</method>
  <param>password_field</param>
  <evidence>&lt;input id=&quot;password_field&quot; size=&quot;30&quot; type=&quot;password&quot;&gt;</evidence>
  </instance>
  </instances>
  <count>1</count>
  <solution>&lt;p&gt;Turn off the AUTOCOMPLETE attribute in forms or individual input elements containing password inputs by using AUTOCOMPLETE=&apos;OFF&apos;.&lt;/p&gt;</solution>
  <reference>&lt;p&gt;http://www.w3schools.com/tags/att_input_autocomplete.asp&lt;/p&gt;&lt;p&gt;https://msdn.microsoft.com/en-us/library/ms533486%28v=vs.85%29.aspx&lt;/p&gt;</reference>
  <cweid>525</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10020</pluginid>
  <alert>X-Frame-Options Header Not Set</alert>
  <name>X-Frame-Options Header Not Set</name>
  <riskcode>2</riskcode>
  <confidence>2</confidence>
  <riskdesc>Medium (Medium)</riskdesc>
  <desc>&lt;p&gt;X-Frame-Options header is not included in the HTTP response to protect against &apos;ClickJacking&apos; attacks.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://localhost:7272/</uri>
  <method>GET</method>
  <param>X-Frame-Options</param>
  </instance>
  </instances>
  <count>1</count>
  <solution>&lt;p&gt;Most modern Web browsers support the X-Frame-Options HTTP header. Ensure it&apos;s set on all web pages returned by your site (if you expect the page to be framed only by pages on your server (e.g. it&apos;s part of a FRAMESET) then you&apos;ll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. ALLOW-FROM allows specific websites to frame the web page in supported web browsers).&lt;/p&gt;</solution>
  <reference>&lt;p&gt;http://blogs.msdn.com/b/ieinternals/archive/2010/03/30/combating-clickjacking-with-x-frame-options.aspx&lt;/p&gt;</reference>
  <cweid>16</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10016</pluginid>
  <alert>Web Browser XSS Protection Not Enabled</alert>
  <name>Web Browser XSS Protection Not Enabled</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;Web Browser XSS Protection is not enabled, or is disabled by the configuration of the &apos;X-XSS-Protection&apos; HTTP response header on the web server&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://localhost:7272/</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  </instances>
  <count>1</count>
  <solution>&lt;p&gt;Ensure that the web browser&apos;s XSS filter is enabled, by setting the X-XSS-Protection HTTP response header to &apos;1&apos;.&lt;/p&gt;</solution>
  <otherinfo>&lt;p&gt;The X-XSS-Protection HTTP response header allows the web server to enable or disable the web browser&apos;s XSS protection mechanism. The following values would attempt to enable it: &lt;/p&gt;&lt;p&gt;X-XSS-Protection: 1; mode=block&lt;/p&gt;&lt;p&gt;X-XSS-Protection: 1; report=http://www.example.com/xss&lt;/p&gt;&lt;p&gt;The following values would disable it:&lt;/p&gt;&lt;p&gt;X-XSS-Protection: 0&lt;/p&gt;&lt;p&gt;The X-XSS-Protection HTTP response header is currently supported on Internet Explorer, Chrome and Safari (WebKit).&lt;/p&gt;&lt;p&gt;Note that this alert is only raised if the response body could potentially contain an XSS payload (with a text-based content type, with a non-zero length).&lt;/p&gt;</otherinfo>
  <reference>&lt;p&gt;https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet&lt;/p&gt;&lt;p&gt;https://blog.veracode.com/2014/03/guidelines-for-setting-security-headers/&lt;/p&gt;</reference>
  <cweid>933</cweid>
  <wascid>14</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10021</pluginid>
  <alert>X-Content-Type-Options Header Missing</alert>
  <name>X-Content-Type-Options Header Missing</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;The Anti-MIME-Sniffing header X-Content-Type-Options was not set to &apos;nosniff&apos;. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://localhost:7272/</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  <instance>
  <uri>http://localhost:7272/demo.css</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  </instances>
  <count>2</count>
  <solution>&lt;p&gt;Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to &apos;nosniff&apos; for all web pages.&lt;/p&gt;&lt;p&gt;If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.&lt;/p&gt;</solution>
  <otherinfo>&lt;p&gt;This issue still applies to error type pages (401, 403, 500, etc) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.&lt;/p&gt;&lt;p&gt;At &quot;High&quot; threshold this scanner will not alert on client or server error responses.&lt;/p&gt;</otherinfo>
  <reference>&lt;p&gt;http://msdn.microsoft.com/en-us/library/ie/gg622941%28v=vs.85%29.aspx&lt;/p&gt;&lt;p&gt;https://www.owasp.org/index.php/List_of_useful_HTTP_headers&lt;/p&gt;</reference>
  <cweid>16</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
</alerts></site><site name="http://127.0.0.1:7272" host="127.0.0.1" port="7272" ssl="false"><alerts><alertitem>
  <pluginid>10021</pluginid>
  <alert>X-Content-Type-Options Header Missing</alert>
  <name>X-Content-Type-Options Header Missing</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;The Anti-MIME-Sniffing header X-Content-Type-Options was not set to &apos;nosniff&apos;. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://127.0.0.1:7272/demo.css</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/welcome.html</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/error.html</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  </instances>
  <count>5</count>
  <solution>&lt;p&gt;Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to &apos;nosniff&apos; for all web pages.&lt;/p&gt;&lt;p&gt;If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.&lt;/p&gt;</solution>
  <otherinfo>&lt;p&gt;This issue still applies to error type pages (401, 403, 500, etc) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.&lt;/p&gt;&lt;p&gt;At &quot;High&quot; threshold this scanner will not alert on client or server error responses.&lt;/p&gt;</otherinfo>
  <reference>&lt;p&gt;http://msdn.microsoft.com/en-us/library/ie/gg622941%28v=vs.85%29.aspx&lt;/p&gt;&lt;p&gt;https://www.owasp.org/index.php/List_of_useful_HTTP_headers&lt;/p&gt;</reference>
  <cweid>16</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10016</pluginid>
  <alert>Web Browser XSS Protection Not Enabled</alert>
  <name>Web Browser XSS Protection Not Enabled</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;Web Browser XSS Protection is not enabled, or is disabled by the configuration of the &apos;X-XSS-Protection&apos; HTTP response header on the web server&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://127.0.0.1:7272/favicon.ico</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/sitemap.xml</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/welcome.html</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/error.html</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/robots.txt</uri>
  <method>GET</method>
  <param>X-XSS-Protection</param>
  </instance>
  </instances>
  <count>7</count>
  <solution>&lt;p&gt;Ensure that the web browser&apos;s XSS filter is enabled, by setting the X-XSS-Protection HTTP response header to &apos;1&apos;.&lt;/p&gt;</solution>
  <otherinfo>&lt;p&gt;The X-XSS-Protection HTTP response header allows the web server to enable or disable the web browser&apos;s XSS protection mechanism. The following values would attempt to enable it: &lt;/p&gt;&lt;p&gt;X-XSS-Protection: 1; mode=block&lt;/p&gt;&lt;p&gt;X-XSS-Protection: 1; report=http://www.example.com/xss&lt;/p&gt;&lt;p&gt;The following values would disable it:&lt;/p&gt;&lt;p&gt;X-XSS-Protection: 0&lt;/p&gt;&lt;p&gt;The X-XSS-Protection HTTP response header is currently supported on Internet Explorer, Chrome and Safari (WebKit).&lt;/p&gt;&lt;p&gt;Note that this alert is only raised if the response body could potentially contain an XSS payload (with a text-based content type, with a non-zero length).&lt;/p&gt;</otherinfo>
  <reference>&lt;p&gt;https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet&lt;/p&gt;&lt;p&gt;https://blog.veracode.com/2014/03/guidelines-for-setting-security-headers/&lt;/p&gt;</reference>
  <cweid>933</cweid>
  <wascid>14</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10020</pluginid>
  <alert>X-Frame-Options Header Not Set</alert>
  <name>X-Frame-Options Header Not Set</name>
  <riskcode>2</riskcode>
  <confidence>2</confidence>
  <riskdesc>Medium (Medium)</riskdesc>
  <desc>&lt;p&gt;X-Frame-Options header is not included in the HTTP response to protect against &apos;ClickJacking&apos; attacks.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://127.0.0.1:7272/</uri>
  <method>GET</method>
  <param>X-Frame-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272</uri>
  <method>GET</method>
  <param>X-Frame-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/welcome.html</uri>
  <method>GET</method>
  <param>X-Frame-Options</param>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/error.html</uri>
  <method>GET</method>
  <param>X-Frame-Options</param>
  </instance>
  </instances>
  <count>4</count>
  <solution>&lt;p&gt;Most modern Web browsers support the X-Frame-Options HTTP header. Ensure it&apos;s set on all web pages returned by your site (if you expect the page to be framed only by pages on your server (e.g. it&apos;s part of a FRAMESET) then you&apos;ll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. ALLOW-FROM allows specific websites to frame the web page in supported web browsers).&lt;/p&gt;</solution>
  <reference>&lt;p&gt;http://blogs.msdn.com/b/ieinternals/archive/2010/03/30/combating-clickjacking-with-x-frame-options.aspx&lt;/p&gt;</reference>
  <cweid>16</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
<alertitem>
  <pluginid>10012</pluginid>
  <alert>Password Autocomplete in Browser</alert>
  <name>Password Autocomplete in Browser</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;The AUTOCOMPLETE attribute is not disabled on an HTML FORM/INPUT element containing password type input.  Passwords may be stored in browsers and retrieved.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://127.0.0.1:7272</uri>
  <method>GET</method>
  <param>password_field</param>
  <evidence>&lt;input id=&quot;password_field&quot; size=&quot;30&quot; type=&quot;password&quot;&gt;</evidence>
  </instance>
  <instance>
  <uri>http://127.0.0.1:7272/</uri>
  <method>GET</method>
  <param>password_field</param>
  <evidence>&lt;input id=&quot;password_field&quot; size=&quot;30&quot; type=&quot;password&quot;&gt;</evidence>
  </instance>
  </instances>
  <count>2</count>
  <solution>&lt;p&gt;Turn off the AUTOCOMPLETE attribute in forms or individual input elements containing password inputs by using AUTOCOMPLETE=&apos;OFF&apos;.&lt;/p&gt;</solution>
  <reference>&lt;p&gt;http://www.w3schools.com/tags/att_input_autocomplete.asp&lt;/p&gt;&lt;p&gt;https://msdn.microsoft.com/en-us/library/ms533486%28v=vs.85%29.aspx&lt;/p&gt;</reference>
  <cweid>525</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
</alerts></site><site name="http://detectportal.firefox.com" host="detectportal.firefox.com" port="80" ssl="false"><alerts><alertitem>
  <pluginid>10021</pluginid>
  <alert>X-Content-Type-Options Header Missing</alert>
  <name>X-Content-Type-Options Header Missing</name>
  <riskcode>1</riskcode>
  <confidence>2</confidence>
  <riskdesc>Low (Medium)</riskdesc>
  <desc>&lt;p&gt;The Anti-MIME-Sniffing header X-Content-Type-Options was not set to &apos;nosniff&apos;. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.&lt;/p&gt;</desc>
  <instances>
  <instance>
  <uri>http://detectportal.firefox.com/success.txt</uri>
  <method>GET</method>
  <param>X-Content-Type-Options</param>
  </instance>
  </instances>
  <count>1</count>
  <solution>&lt;p&gt;Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to &apos;nosniff&apos; for all web pages.&lt;/p&gt;&lt;p&gt;If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.&lt;/p&gt;</solution>
  <otherinfo>&lt;p&gt;This issue still applies to error type pages (401, 403, 500, etc) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.&lt;/p&gt;&lt;p&gt;At &quot;High&quot; threshold this scanner will not alert on client or server error responses.&lt;/p&gt;</otherinfo>
  <reference>&lt;p&gt;http://msdn.microsoft.com/en-us/library/ie/gg622941%28v=vs.85%29.aspx&lt;/p&gt;&lt;p&gt;https://www.owasp.org/index.php/List_of_useful_HTTP_headers&lt;/p&gt;</reference>
  <cweid>16</cweid>
  <wascid>15</wascid>
  <sourceid>3</sourceid>
</alertitem>
</alerts></site></OWASPZAPReport>