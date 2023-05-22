<template>
  <div class="bottom">
    <div class="footer">
        <div class="useful-link">
            <div class="footer-title">
                Useful Links
            </div>
            <ul>
                <li><router-link :to="{name:'home'}">Home</router-link></li>
                <li><a href="">About us</a></li>
                <li><a href="">Product</a></li>
                <li><a href="">Services</a></li>
                <li><a href="">Legal</a></li>
                <li><router-link :to="{name:'contact'}">Contact us</router-link></li>
            </ul>
        </div>
        <div class="about-us">
            <div class="footer-title">
                About us
            </div>
            <p>We are a team of passionate people whose goal is to improve everyone's life through disruptive products. We build great products to solve your business problems.</p>
            <p>Our products are designed for small to medium size companies willing to optimize their performance.</p>
        </div>
        <div class="connect">
            <div class="footer-title">
                Connect with us
            </div>
            <div>
                <div><router-link :to="{name:'contact'}">Contact us</router-link></div>
                <div><a href="mailto: someone@example.com">info@yourcompany.example.com</a></div>
                <div><a href="tel:+1234567890">+1 (650) 555-0111</a></div>
            </div>
        </div>
    </div>
    <div class="copy-right">
        Copyright © Company name
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
    .footer{
        display: flex;
        background: #383E45;
        height: 300px;
        color:white;
        padding: 70px 20% 16px;
    }
    .footer a{
        line-height: 24px;
        color: #66ccca;
    }

    a:hover{
        color: #28918f;
        text-decoration: underline;
    }
    .footer-title{
        margin-bottom: 10px;
        font-size: 20px;
    }
    .useful-link{
        width: 15%;
    }
    .about-us{
        line-height: 24px;
        width: 50%;
        padding: 0 70px 0 20px;
    }
    .about-us p{
        margin-bottom: 10px;
    }
    .connect{
        width: 35%;
    }
    .copy-right{
        color: rgba(255, 255, 255, 0.7);
        padding: 20px 20%;
        height: 56px;
        background: #30343b;
    }
</style>