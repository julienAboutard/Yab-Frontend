<script>
export default {
    data() {
        return {
            apprenants: null,
            new_appr_nom: '',
            new_appr_prenom: '',
            messages: []
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
                } else {  // 200
                    this.messages.push(`Apprenant ${result.appr_prenom} ${result.appr_nom} ajouté avec succès!`)
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });

        }
    },
    mounted() {
        this.fetchApprs()
    }
}
</script>

<template>
    <ul v-for="message in this.messages">
        <li>{{ message }}</li>
    </ul>
    <p v-if="!apprenants">Loading...</p>
    <div v-else>
        <ul v-for="appr in this.apprenants">
            <li>{{appr.appr_prenom}} {{appr.appr_nom}}</li>
        </ul>
    </div>
    <form @submit.prevent="addAppr">
        <label for="nom">nom</label>
        <input name="nom" v-model="new_appr_nom">
        <label for="prenom">nom</label>
        <input name="prenom" v-model="new_appr_prenom">
        <button>Ajouter un apprenant</button>
    </form>
</template>