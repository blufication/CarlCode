

// function for creating the designed box for the bot messages
function create_in_html(msg) {

//creating the  message text paragraph
var in_message_p = document.createElement("p");
var in_html_p = document.createTextNode(msg);
in_message_p.appendChild(in_html_p);

//creating the data block
var d = new Date();
var in_message_t = document.createElement("span");
var in_html_t = document.createTextNode(d.toLocaleTimeString());
in_message_t.className="in-time";
in_message_t.appendChild(in_html_t);

//merging both time and text boxes
var in_message_in = document.createElement("div");
in_message_in.className="received-msg-inbox";
in_message_in.appendChild(in_message_p);
in_message_in.appendChild(in_message_t);

//inserting int another container
var in_message_rm = document.createElement("div");
in_message_rm.className="received-msg";
in_message_rm.appendChild(in_message_in);

//inserting into another container
var in_message_rc = document.createElement("div");
in_message_rc.className="received-chats";
in_message_rc.appendChild(in_message_rm);

//appending to the element with id "msg-page"
var element_in = document.getElementById("msg-page");
element_in.appendChild(in_message_rc);
}

// function for creating the designed box for the bot messages
function create_out_html(msg) {

//creating the  message text paragraph
var out_message_p = document.createElement("p");
var out_html_p = document.createTextNode(msg);
out_message_p.appendChild(out_html_p);

//creating the data block
var d = new Date();
var out_message_t = document.createElement("span");
var out_html_t = document.createTextNode(d.toLocaleTimeString());
out_message_t.className="out-time";
out_message_t.appendChild(out_html_t);

//merging both time and text boxes
var out_message_in = document.createElement("div");
out_message_in.className="outgoing-msg-inbox";
out_message_in.appendChild(out_message_p);
out_message_in.appendChild(out_message_t);

//inserting int another container
var out_message_om = document.createElement("div");
out_message_om.className="outgoing-msg";
out_message_om.appendChild(out_message_in);

//inserting into another container
var out_message_oc = document.createElement("div");
out_message_oc.className="outgoing-chats";
out_message_oc.appendChild(out_message_om);

//appending to the element with id "msg-page"
var element_out = document.getElementById("msg-page");
element_out.appendChild(out_message_oc);
}