<script>
export default {
    data() {
        return {
            apprenants: null,
            new_appr_nom: '',
            new_appr_prenom: '',
            cur_appr_nom: '',
            cur_appr_prenom: '',
            messages: [],
            msg_class: "success_msg"
        }
    },
    methods: {
        clearMessages(){
            this.messages = []
        },
        async fetchApprs() {
            console.log("Fetching apprenants")
            const res = await fetch(
                `http://127.0.0.1:8000/api/apprenants/`
            )
            this.apprenants = await res.json()
        },
        hide_all() {
            console.log(`Will hide all update forms`)
            this.apprenants.forEach(appr => {
                console.log(`f_update_${appr.id}`)
                this.$refs[`f_update_${appr.id}`][0].style.display = 'none'
            });
        },
        async addAppr() {
            fetch("http://127.0.0.1:8000/api/apprenants/", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "appr_nom": this.new_appr_nom,
                    "appr_prenom": this.new_appr_prenom
                })
            })
            .then( (response) => {
                this.clearMessages()
                if ((response.status > 200 && response.status < 300) || response.status == 400) {
                    return new Promise((resolve) => response.json()
                        .then((result) => resolve({
                        status: response.status,
                        result,
                    })));
                } else {
                    throw Error(response.statusText);
                }
            })
            .then(({status, result}) => {
                console.log("Result: ", result)
                console.log("Status: ", status)
                if (status == 400){
                    for (const [key, value] of Object.entries(result)) {
                        this.messages.push(`Erreur pour le champ ${key}: ${value}`)
                    }
                    this.msg_class = "err_msg"
                } else {  // 200
                    this.messages.push(`Apprenant ${result.appr_prenom} ${result.appr_nom} ajouté avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchApprs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        async updateAppr(appr_id) {
            fetch(`http://127.0.0.1:8000/api/apprenants/${appr_id}/`, {
                method: "PATCH",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "appr_nom": this.cur_appr_nom,
                    "appr_prenom": this.cur_appr_prenom
                })
            })
            .then( (response) => {
                this.clearMessages()
                if (response.status == 200 || response.status == 400) {
                    return new Promise((resolve) => response.json()
                        .then((result) => resolve({
                        status: response.status,
                        result,
                    })));
                } else {
                    throw Error(response.statusText);
                }
            })
            .then(({status, result}) => {
                console.log("Result: ", result)
                console.log("Status: ", status)
                if (status == 400){
                    for (const [key, value] of Object.entries(result)) {
                        this.messages.push(`Erreur pour le champ ${key}: ${value}`)
                    }
                    this.msg_class = "err_msg"
                } else {  // 200
                    this.messages.push(`Apprenant ${result.appr_prenom} ${result.appr_nom} mis à jour avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchApprs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        },
        async deleteAppr(appr_id, appr_nom, appr_prenom) {
            if(confirm(`Voulez vous vraiment supprimer ${appr_nom} ${appr_prenom} ?`)){
                fetch(`http://127.0.0.1:8000/api/apprenants/${appr_id}/`, {
                    method: "DELETE",
                })
                .then( (response) => {
                    this.clearMessages()
                    if (response.status == 204) {
                        this.messages.push(`Apprenant supprimé avec succès!`)
                        this.msg_class = "succes_msg"
                        this.hide_all()
                        this.fetchApprs()
                    } else {
                        throw Error(response.statusText);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            }
        },
        show(appr_id) {
            console.log(`Will display appr #${appr_id} update form`)
            this.apprenants.forEach(appr => {
                console.log(`f_update_${appr.id}`)
                this.$refs[`f_update_${appr.id}`][0].style.display = 'none'
                if (appr.id == appr_id){
                    this.cur_appr_nom = appr.appr_nom
                    this.cur_appr_prenom = appr.appr_prenom
                }
            });
            this.$refs[`f_update_${appr_id}`][0].style.display = 'block'
        }
    },
    mounted() {
        this.fetchApprs()
    }
}
</script>

<template>
    <v-list-item :class="msg_class">
        <v-list-item-content v-for="message in this.messages">
            {{ message }}
        </v-list-item-content>
    </v-list-item>

    <p v-if="!apprenants">Loading...</p>
    <v-list v-else>
        <v-container>
            <v-list-item 
                v-for="(appr,i) in this.apprenants"
                v:key="i">
                <v-card>
                    <v-list-item-content>
                        <v-list-item-title v-text="appr.appr_prenom +' '+ appr.appr_nom"></v-list-item-title>
                        <a href="#" @click="show(appr.id)">Modifier</a> |&nbsp;
                        <a href="#" @click="deleteAppr(appr.id, appr.appr_prenom, appr.appr_nom)">Supprimer</a>
                        <br>
                        <form style="display: none;" :ref="'f_update_' + appr.id" @submit.prevent="updateAppr(appr.id)">
                            <v-container>
                                <v-text-field v-model="cur_appr_nom"></v-text-field>
                                <v-text-field v-model="cur_appr_prenom"></v-text-field>
                                <v-btn @click="updateAppr(appr.id)">Mettre à jour</v-btn>
                            </v-container>
                        </form>
                    </v-list-item-content>
                </v-card>
            </v-list-item>
        </v-container>    
    </v-list>
    <br>
    <h2>Ajouter un apprenant</h2>
    <v-form @submit.prevent="addAppr">
        <v-container>
            <v-text-field v-model="new_appr_prenom" label="Prénom"></v-text-field>
            <v-text-field v-model="new_appr_nom" label="Nom"></v-text-field>
            <v-btn @click="addAppr">Ajouter</v-btn>
        </v-container>
    </v-form>
</template>

<style>
.err_msg {
    color: red;
}
.succes_msg {
    color: green;
}
.v-card {
    background-color: blue;
}
</style>