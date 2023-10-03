// const URL = 'https://magnifier.onrender.com/';
const URL = 'http://127.0.0.1:5000/';
const resultDiv = $('#resultCollapse');
const default_image = '/static/images/profile_pics/default_image.png';

async function register(evt) {
  const username = $('#registerUsername').val();
  const first_name = $('#registerFirstName').val();
  const last_name = $('#registerLastName').val();
  const email = $('#registerEmail').val();
  const pwd = $('#registerPWD').val();
  const data = { username, first_name, last_name, pwd, email };
  const response = await axios.post(`${URL}/magnifier/register`, data);
  if (response.data.response === 'Email already registered') {
    $('#alert').empty();
    $('#alert').append(
      '<div class="alert alert-danger text-center w-0" role="alert"> This email has already been registered in our system.</div>'
    );
  }
  if (response.data.response === 'Username already registered') {
    $('#alert').empty();
    $('#alert').append(
      '<div class="alert alert-danger text-center w-0" role="alert">Sorry, but this username is already in use.</div>'
    );
  } else if (response.data.response === 'Successful registration') {
    window.location = `/magnifier/${username}`;
  }
}

async function authenticate(evt) {
  let username = $('#username').val();
  let password = $('#password').val();
  let data = { username, password };
  const response = await axios.post(`${URL}/login`, data);
  if (response.data.response == 'Invalid user') {
    $('#alert').empty();
    $('#alert').append(
      '<div class="alert alert-danger text-center w-0" role="alert">User not found or the password is incorrect!</div>'
    );
  } else {
    window.location = `/magnifier/${username}`;
  }
}

fetchResult = async function (type) {
  const username = $('#userUsername').text();
  if (type == 'PHONE') {
    const countryCode = $('#countryCode').val();
    const phoneNumber = $('#phoneNumber').val();
    let values = { countryCode, phoneNumber, type };
    const { data } = await axios.post(`${URL}/${username}/search`, values);
    return data;
  } else if (type == 'EMAIL') {
    const emailAddress = $('#emailAddress').val();
    let values = { emailAddress, type };
    const { data } = await axios.post(`${URL}/${username}/search`, values);
    return data;
  } else if (type == 'VAT') {
    const vatNumber = $('#vatNumber').val();
    const countryVat = $('#countryVatCode').val();
    let values = { vatNumber, type, countryVat };
    const { data } = await axios.post(`${URL}/${username}/search`, values);
    return data;
  } else if (type == 'DOMAIN') {
    const domainAddress = $('#domainAddress').val();
    let values = { domainAddress, type };
    const { data } = await axios.post(`${URL}/${username}/search`, values);
    return data;
  }
  return data;
};

addErrorWarning = function () {
  $(resultDiv).empty();
  $(resultDiv).append(
    '<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong></strong>We are sorry! The data that you have provided didn\'t return any valid result or we are currently experiencing a problem with the server.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
  );
  $('#resultCollapse').collapse('show');
};

addResult = function (result) {
  $(resultDiv).empty();
  if (result.type === false) {
    $(resultDiv).append(
      '<div class="alert alert-warning alert-dismissible fade show" role="alert"><strong></strong>We are sorry! The data that you have provided didn\'t return any valid result.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    );
  } else {
    if (result.type === 'Email') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv"><span class="text-center  mb-2">Search Result:</span>
        <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Email Address: ${result.email}</span>
        <span>Is the email free: ${result.free_email}</span>
        <span>Is the email valid: ${result.valid}</span>
        <span>Is the email disposable: ${result.disposable}</span>
        <br>
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong><small>Search results are automatically saved on the user's profile and can be accessed through the user infomation link.</strong></small>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
       </div>
      </div>`
      );
    } else if (result.type === 'Vat') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv"><span class="text-center  mb-2">Search Result:</span>
      <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Vat Number: ${result.vat_number}</span>
        <span>Company name: ${result.company_name}</span>
        <span>Company address : ${result.company_address}</span>
        <span>Is this VAT valid? ${result.valid}</span>
        <br>
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong><small>Search results are automatically saved on the user's profile and can be accessed through the user infomation link.</strong></small> 
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
       </div>
      </div>`
      );
    } else if (result.type === 'Phone') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv"><span class="text-center  mb-2">Search Result:</span>
      <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Phone Number: ${result.prefix}${result.phone_number}</span>
        <span>Prefix: ${result.prefix}</span>
        <span>Local: ${result.local}</span>
        <span>Country: ${result.country}</span>
        <span>Location: ${result.location}</span>
        <span>Type: ${result.phone_type}</span>
        <span>Carrier: ${result.carrier}</span>
        <br>
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong><small>Search results are automatically saved on the user's profile and can be accessed through the user infomation link.</strong></small>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
       </div>
      </div>`
      );
    } else if (result.type === 'Domain') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv"><span class="text-center  mb-2">Search Result:</span>
      <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Domain: ${result.domain}</span>
        <span>Name: ${result.name}</span>
        <span>Locality: ${result.locality}</span>
        <span>Country: ${result.country}</span>
        <span>Industry: ${result.industry}</span>
        <span>Founded in: ${result.year_founded}</span>
        <span>Number of employees: ${result.employees_count}</span>
        <span>Linkedin: <a href="http://www.${result.linkedin}">${result.linkedin}</a></span>
        <br>
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong><small>Search results are automatically saved on the user's profile and can be accessed through the user infomation link.</strong></small>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
       </div>
      </div>`
      );
    }
  }
  $('#searchCount').text(result.count);
  $('#resultCollapse').collapse('show');
};

$('#registerForm').on('submit', function (evt) {
  evt.preventDefault();
  register();
});

$('#authForm').on('submit', function (evt) {
  evt.preventDefault();
  authenticate();
});

$('#phoneSearchForm').on('submit', async function (evt) {
  evt.preventDefault();
  const type = $('#phoneType').text();
  try {
    const result = await fetchResult(type);
    addResult(result);
  } catch (err) {
    addErrorWarning();
  }
  this.reset();
});

$('#emailSearchForm').on('submit', async function (evt) {
  evt.preventDefault();
  const type = $('#emailType').text();
  try {
    const result = await fetchResult(type);

    addResult(result);
  } catch (err) {
    addErrorWarning();
  }
  this.reset();
});

$('#vatSearchForm').on('submit', async function (evt) {
  evt.preventDefault();
  const type = $('#vatType').text();
  try {
    const result = await fetchResult(type);
    addResult(result);
  } catch (err) {
    addErrorWarning();
  }
  this.reset();
});

$('#domainSearchForm').on('submit', async function (evt) {
  evt.preventDefault();
  const type = $('#domainType').text();
  try {
    const result = await fetchResult(type);
    addResult(result);
  } catch (err) {
    addErrorWarning();
  }
  this.reset();
});

$('#editButton').on('click', function (evt) {
  $('#userInfo').collapse('toggle');
  $('#userImage').toggleClass('opacity-50');
  $('#editPicture').toggle();
  $(this).toggle();
});

$('#cancelEdit').on('click', function (evt) {
  $('#userInfo').collapse('toggle');
  $('#userImage').toggleClass('opacity-50');
  $('#editPicture').toggle();
  $('#editButton').toggle();
});

editPic = async function (image) {
  $('#userImage').attr('src', '');
  const username = $('#userUsername').text();
  try {
    const { data } = await axios.patch(`${URL}/${username}/picture`, { image });
    $('#userImage').attr('src', data.image);
  } catch {
    $('#userImage').attr('src', default_image);
  }
};

$('#imageFile').on('change', async function (evt) {
  const image = this.files[0];
  function result(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    return new Promise((resolve, reject) => {
      reader.addEventListener('load', () => {
        resolve(reader.result);
      });
    });
  }
  const imageURL = await result(image);
  $('#imageFile').val('');
  editPic(imageURL);
});

$('#deletePicture').on('click', async function (evt) {
  const image = '';
  $('#imageFile').val('');
  editPic(image);
});

$('#editForm').on('submit', async function (evt) {
  evt.preventDefault();
  const username = $('#userUsername').text();
  const newUsername = $('#newUsername').val();
  const email = $('#email').val();
  const { data } = await axios.patch(`${URL}/${username}/edit`, {
    username,
    newUsername,
    email,
  });
  $('#username').val(data.username);
  $('#userUsername').text(data.username);
  $('#email').val(data.email);
  $('#userEmail').text(`Email: ${data.email}`);
  $('#editButton').toggle();
  $('#userImage').toggleClass('opacity-50');
  $('#editPicture').toggle();
  $('#userInfo').collapse('toggle');
});

$('.deleteSearch').on('click', async function (evt) {
  const username = $('#userUsername').text();
  const searchId = $(this).attr('id');
  const parent = $(this).parents().get(4);
  let values = { username, searchId };
  const { data } = await axios.post(`${URL}/${searchId}/delete`, values);
  $('#searchesLength').text(data.count);
  $(parent).remove();
});

$('#newSearchBtn').on('click', function (evt) {
  $('#collapseVat').collapse('hide');
  $('#collapseEmail').collapse('hide');
  $('#collapsePhone').collapse('hide');
  $('#collapseDomain').collapse('hide');
  $('#resultCollapse').collapse('hide');
});

$('#phoneSearch').on('click', function (evt) {
  $('#collapseVat').collapse('hide');
  $('#collapseEmail').collapse('hide');
  $('#collapseDomain').collapse('hide');
  $('#resultCollapse').collapse('hide');
});
$('#emailSearch').on('click', function (evt) {
  $('#collapseVat').collapse('hide');
  $('#collapsePhone').collapse('hide');
  $('#collapseDomain').collapse('hide');
  $('#resultCollapse').collapse('hide');
});
$('#vatSearch').on('click', function (evt) {
  $('#collapsePhone').collapse('hide');
  $('#collapseEmail').collapse('hide');
  $('#collapseDomain').collapse('hide');
  $('#resultCollapse').collapse('hide');
});

$('#domainSearch').on('click', function (evt) {
  $('#collapsePhone').collapse('hide');
  $('#collapseEmail').collapse('hide');
  $('#collapseVat').collapse('hide');
  $('#resultCollapse').collapse('hide');
});
