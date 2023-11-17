const URL = 'https://magnifier.onrender.com';
const resultDiv = $('#resultCollapse');

fetchResult = async function (type) {
  const username = $('#userUsername').text();
  if (type == 'PHONE') {
    const countryCode = $('#countryCode').val();
    const phoneNumber = $('#phoneNumber').val();
    let values = { countryCode, phoneNumber, type };
    const { data } = await axios.post(`${URL}/search`, values);
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
        id="resultDiv">
        <div class="d-flex justify-content-end">
        <button type="button" class="btn-close btn-close-white mt-2"   aria-label="Close" id="closeResultBTN" ></button>
        </div>
        <h4 class="text-center  mb-2">Search Result:</h4>
        <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Email Address: ${result.email}</span>
        <span>Is the email free: ${result.free_email}</span>
        <span>Is the email valid: ${result.valid}</span>
        <span>Is the email disposable: ${result.disposable}</span>
       </div>
      </div>`
      );
    } else if (result.type === 'Vat') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv">
        <div class="d-flex justify-content-end">
        <button type="button" class="btn-close btn-close-white mt-2" aria-label="Close" id="closeResultBTN"></button></div>
        <h4 class="text-center  mb-2">Search Result:</h4>
      <div class="d-flex justify-content-between mt-2">
        <h5>Type: ${result.type}</h4>
        <h5>Search date: ${result.date}</h4>
       </div>
       <div class="d-flex flex-column">
        <span>Vat Number: ${result.vat_number}</span>
        <span>Company name: ${result.company_name}</span>
        <span>Company address : ${result.company_address}</span>
        <span>Is this VAT valid? ${result.valid}</span>
       </div>
      </div>`
      );
    } else if (result.type === 'Phone') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv">
        <div class="d-flex justify-content-end">
        <button type="button" class="btn-close btn-close-white mt-2" aria-label="Close" id="closeResultBTN"></button></div>
        <h4 class="text-center  mb-2">Search Result:</h4>
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
       </div>
      </div>`
      );
    } else if (result.type === 'Domain') {
      $(resultDiv).append(
        `<div class="card card-body bg-black d-inline-block text-center border border-white pt-0 w-100"
        id="resultDiv">
        <div class="d-flex justify-content-end">
        <button type="button" class="btn-close btn-close-white mt-2" aria-label="Close" id="closeResultBTN"></button></div>
        <h4 class="text-center  mb-2">Search Result:</h4>
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
       </div>
      </div>`
      );
    }
  }
  $('#searchCount').text(result.count);
  $('#resultCollapse').collapse('show');
};

$('body').on('click', '#closeResultBTN', function (evt) {
  $(resultDiv).empty();
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
    await addResult(result);
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
