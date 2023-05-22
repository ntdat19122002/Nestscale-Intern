<template>
  <div class="spin"></div>
</template>

<script>
export default {

}
</script>

<style>
    .spin{
        display: block;
        width: 100px;
        height: 100px;
        margin: 50px auto;
        border: 10px solid transparent;
        border-radius: 50%;
        border-top-color: #ff8800;
        animation: spin 1s ease infinite;
    }
    @keyframes spin {
        from {
            transform:rotate(0deg);
        }
        to {
            transform:rotate(360deg);
        }
    }
</style>