<template>
    <div class="container mt-5">
        
        <div v-if="success">
        <h2 class="text-center mb-4">
            Student Profile
        </h2>
            <div class="card p-4">
                <p><b>Name:</b> {{ student.name }}</p>
                <p><b>Email:</b> {{ student.email }}</p>
                <p><b>Phone:</b> {{ student.phone }}</p>
                <p><b>Branch:</b> {{ student.branch }}</p>
                <p><b>Year:</b> {{ student.year }}</p>
               <p><b>CGPA:</b> {{ student.cgpa }}</p>
                <p><b>Skills:</b> {{ student.skills }}</p>
                <p><b>LinkedIn:</b> {{ student.linkedin }}</p>
                <p><b>GitHub:</b> {{ student.github }}</p>
                <a
                    v-if="student.resume_path"
                    :href="'http://127.0.0.1:5000/'+student.resume_path"
                    target="_blank"
                    class="btn btn-primary"
                >
                    View Resume
                </a>
            </div>     
        </div>

        <div v-else>
            <div class="alert alert-danger">
                {{ message }}
            </div>
        </div>

    </div>
</template>

<script>

export default{

    data(){
        return{
            success:false,
            message:"",
            student:{}
        }
    },

    mounted(){
        this.loadStudent()
    },

    methods:{

        async loadStudent(){
            const response=await fetch(
                "http://127.0.0.1:5000/api/company/application/"+this.$route.params.id+"/student",
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            const result=await response.json()
            if(result.success){
                this.success=true
                this.student=result.student
            }
            else{
                this.message=result.message
            }
        }
    }
}

</script>