document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submission of compose form
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load mails in the mailbox
  fetch(`emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(emails => {
    const emailsView = document.querySelector('#emails-view');

    emails.forEach(email => {
      const email_div = document.createElement('div');
      email_div.className = 'email_list';

      email_div.style.backgroundColor = email.read ? 'white' : 'lightgray';
      email_div.addEventListener('click', () => view_mail(email.id, mailbox));

      email_div.innerHTML = `
        <strong>${mailbox === 'sent' ? `To: ${email.recipients}` : `From: ${email.sender}`}</strong>
        ${email.subject}
        <br>
        <small style="color: #757575;font-weight: bold;">${email.timestamp}</small>
      `;

      emailsView.appendChild(email_div);
    });
  })
  .catch(error => {
    console.error('Problem in Fetching mails:', error);
  });
}

function send_mail(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

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
    console.log(result);
    load_mailbox('sent');
  })
  .catch(error => {
    console.error('Error:', error);
  });

  return false;
}

function view_mail(mail_id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Mark email as read
  fetch(`emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

  // Fetch the email data
  fetch(`emails/${mail_id}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(email => {
    const email_view = document.querySelector('#email-view');
    
    email_view.innerHTML = `
      <strong>From: </strong>${email.sender}
      <br>
      <strong>To: </strong>${email.recipients}
      <br>
      <strong>Subject: </strong>${email.subject}
      <br>
      <strong>Timestamp: </strong>${email.timestamp}
      <br>
      <div id="email-actions">
        <button id="reply-button" class="btn btn-sm btn-outline-primary">Reply</button>
        ${mailbox !== 'sent' ? '<button id="archive-button" class="btn btn-sm btn-outline-secondary"></button>' : ''}
      </div>
      <hr>
      ${email.body}
    `;

    const archiveButton = document.querySelector('#archive-button');
    if (archiveButton) {
      archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
      archiveButton.addEventListener('click', () => archive(email));
    }

    const replyButton = document.querySelector('#reply-button');
    replyButton.addEventListener('click', () => reply_email(email));
  });
}

function reply_email(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  document.querySelector('#compose-recipients').value = email.sender;

  let subject = email.subject;
  if (!subject.startsWith("Re: ")) {
    subject = `Re: ${subject}`;
  }
  document.querySelector('#compose-subject').value = subject;

  document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
}

function archive(email) {
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived
    })
  })
  .then(() => load_mailbox('inbox'))
  .catch(error => console.error('Error archiving email:', error));
}
