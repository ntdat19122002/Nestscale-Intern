<template>
  <div class="contact">
    <div class="contact-header">
      <div class="black-ground">
        <div>
          Contact us
        </div>
      </div>
    </div>
    <div class="main-contact">
      <div class="contact-form">
        <p>Contact us about anything related to our company or services.</p>
        <p>We'll do our best to get back to you as soon as possible.</p>
        
        <form action="">
          <div>
            <label>Your Name *</label>
            <input type="text" required>
          </div>
          <div>
            <label>Phone Number</label>
            <input type="text">
          </div>
          <div>
            <label>Email *</label>
            <input type="text" required>
          </div>
          <div>
            <label>Your Company</label>
            <input type="text">
          </div>
          <div>
            <label>Subject *</label>
            <input type="text" required>
          </div>
          <div>
            <label>Your Question</label>
            <input type="text">
          </div>
          <button class="mini-button">Submit</button>
        </form>
      </div>
      <div class="contact-info">
        <div>YourCompany</div>
        <pre>
250 Executive Park Blvd, Suite 3400
San Francisco CA 94134
United States</pre>
        <div>+1 (650) 555-0111</div>
        <div>info@yourcompany.com</div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
    .contact-header{
      height: 110px;
      background-image: url('../../static/images/banner/contact.png');
    }

    .black-ground{
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      color: white;
      display: flex;
      align-items: center;
      padding: 0 19.5%;
      font-size: 35px;
    }

    .contact p{
      line-height: 24px;
    }

    .main-contact{
      padding: 20px 19.5%;
      display: flex;
    }
    .contact-form{
      width: 50%;
    }

    form{
      padding: 20px 0;
      font-size: 20px;
    }

    form button{
      font-size: 20px;
      margin: 10px 0 0 250px;
    }

    form div{
      margin: 10px 0;
      display: flex;
      justify-content: space-between;
    }
    form div label{
      font-weight: bold;
    }
    form div input{
      padding: 10px;
      margin-right: 30px;
      width: 300px;
    }
    .contact-info{
      margin-left: 20%;
    }
</style>