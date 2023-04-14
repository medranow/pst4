document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send an e-mail
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Function that opens compose view pre filled
function reply_email(id){

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
          // Show compose view and hide other views
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#email-detail-view').style.display = 'none';
      
        // Clear out composition fields
        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if (subject.split(' ',1)[0] != "Re:") {
          subject = "Re: " + email.subject;
        } 
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
    });

}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
  
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-detail-view').style.display = 'block';

    document.querySelector('#email-detail-view').innerHTML = `
    <h5><strong>Sender: ${email.sender}</h5>
    <h5> <strong>Recipients:</strong>${email.recipients}</h5>
    <h5><strong>Subject:</strong> ${email.subject}</h5>
    <h5><strong>Timestamp:</strong> ${email.timestamp}</h5>
    <h6>${email.body}</h6>
    `;

    // Check if read
    if (!email.read){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

    // Archive/Unarchive logic
    const button_arch = document.createElement('button');
    button_arch.innerHTML = email.archived ? "Unarchived" : "Archived";
    button_arch.className = email.archived ? "btn btn-success" : "btn btn-warning";
    button_arch.addEventListener('click', function() {
      console.log('This element has been clicked!');

      // Set status in logic to archived/unarchived
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
      .then(() => { load_mailbox('inbox')})
    });
    document.querySelector('#email-detail-view').append(button_arch);

    // Reply Button
    const button_reply = document.createElement('button');
    button_reply.innerHTML = "Reply";
    button_reply.className = "btn btn-success m-2";
    button_reply.addEventListener('click', function() {
      console.log("Reply button clicked");

      // Open the compose mail function pre-loaded
      reply_email(id);
    });
    document.querySelector('#email-detail-view').append(button_reply);
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load appropiate mailbox with content
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      //Iterate over emails and create div for each
      emails.forEach(item => {

        console.log(item);

        // Create div for each email
        const element = document.createElement('div');
        element.className = item.read ? 'list-group-item-dark border border-dark m-2 p-2' : 'list-group-item-light border border-dark m-2 p-2';
        element.innerHTML = `
        <h4>Sender: ${item.sender}</h4>
        <h4>Subject: ${item.subject}</h4>
        <p>${item.timestamp}</p>
        `;

         // Add event to view email
         element.addEventListener('click', function(){
          view_email(item.id);
         });

        // Append email to the div id
        document.querySelector('#emails-view').append(element);
      })
  });
}

function send_email(event) {
  // Allows me to see what happened to my event
  event.preventDefault();

  // Store fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send data to backend (API)
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
}



