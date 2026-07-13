<template>

<div class="container mt-5">

    <h2 class="text-center mb-4">
        My Offers
    </h2>

    <div
        v-if="message"
        class="alert alert-warning"
    >
        {{ message }}
    </div>

    <div v-if="success">

        <table class="table table-bordered table-striped">

            <thead>

                <tr>

                    <th>Company</th>
                    <th>Role</th>
                    <th>Specialization</th>
                    <th>Drive Status</th>
                    <th>Offer Status</th>
                    <th>Action</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="offer in offers"
                    :key="offer.application_id"

                    :class="{
                        'table-danger': offer.drive_status == 'Cancelled',
                        'table-warning': offer.drive_status == 'Closed',
                        'table-success': offer.offer_status == 'Accepted'
                    }"
                >

                    <td>{{ offer.company }}</td>

                    <td>{{ offer.job_title }}</td>

                    <td>{{ offer.specialization }}</td>

                    <td>{{ offer.drive_status }}</td>

                    <td>{{ offer.offer_status }}</td>

                    <td>

                        <div v-if="offer.can_respond">

                            <button
                                class="btn btn-success btn-sm me-2"
                                @click="updateOffer(
                                    offer.application_id,
                                    'Accepted'
                                )"
                            >
                                Accept
                            </button>

                            <button
                                class="btn btn-danger btn-sm"
                                @click="updateOffer(
                                    offer.application_id,
                                    'Rejected'
                                )"
                            >
                                Reject
                            </button>

                        </div>

                        <button
                            v-else-if="offer.offer_status == 'Accepted'"
                            class="btn btn-success btn-sm"
                            disabled
                        >
                            Accepted
                        </button>

                        <button
                            v-else-if="offer.offer_status == 'Rejected'"
                            class="btn btn-secondary btn-sm"
                            disabled
                        >
                            Rejected
                        </button>

                        <button
                            v-else
                            class="btn btn-warning btn-sm"
                            disabled
                        >
                            Cannot Respond
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

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

            success: false,

            message: "",

            offers: []

        }

    },

    mounted(){

        this.loadOffers()

    },

    methods:{

        async loadOffers(){

            const response = await fetch(

                "http://127.0.0.1:5000/api/student/offers",

                {

                    headers:{

                        "Authorization":
                        "Bearer " + localStorage.getItem("token")

                    }

                }

            )

            const result = await response.json()

            if(result.success){

                this.success = true

                this.offers = result.offers

                this.message = ""

                if(result.is_placed){

                    this.message =
                    "You have already accepted an offer."

                }

                else if(!result.is_active){

                    this.message =
                    "Inactive students cannot respond to offers."

                }

            }

            else{

                this.success = false

                this.message = result.message

            }

        },

        async updateOffer(applicationId, offerStatus){

            const response = await fetch(

                "http://127.0.0.1:5000/api/student/update-offer-status/" + applicationId,

                {

                    method: "PUT",

                    headers:{

                        "Authorization":
                        "Bearer " + localStorage.getItem("token"),

                        "Content-Type":"application/json"

                    },

                    body: JSON.stringify({

                        offer_status: offerStatus

                    })

                }

            )

            const result = await response.json()

            alert(result.message)

            this.loadOffers()

        }

    }

}

</script>