<template>

<div class="container mt-5">

<h1>Placement Portal</h1>

<p>{{ message }}</p>

</div>

</template>


<script>

export default {

data() {

return {

message: ""

}

},

mounted() {

fetch("http://127.0.0.1:5000/")

.then(response => response.json())

.then(data => {

this.message = data.message

})

}

}

</script>