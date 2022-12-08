<script>
export default {
    data() {
        return {
            briefs: null,
            new_brief_title: '',
            new_brief_url: '',
            new_brief_nb_apprs: '',
            cur_brief_title: '',
            cur_brief_url: '',
            cur_brief_nb_apprs: '',
            messages: [],
            msg_class: "success_msg"
        }
    },
    methods: {
        clearMessages(){
            this.messages = []
        },
        async fetchBriefs() {
            console.log("Fetching Briefs")
            const res = await fetch(
                `http://127.0.0.1:8000/api/briefs/`
            )
            this.briefs = await res.json()
        },
        hide_all() {
            console.log(`Will hide all update forms`)
            this.briefs.forEach(brief => {
                console.log(`f_update_${brief.id}`)
                this.$refs[`f_update_${brief.id}`][0].style.display = 'none'
            });
        },
        async addBrief() {
            fetch("http://127.0.0.1:8000/api/briefs/", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "brief_title": this.new_brief_title,
                    "brief_url": this.new_brief_url,
                    "brief_nb_apprs": this.new_brief_nb_apprs
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
                    this.messages.push(`Brief ${result.brief_title} ajouté avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchBriefs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        async updateBrief(brief_id) {
            fetch(`http://127.0.0.1:8000/api/briefs/${brief_id}/`, {
                method: "PATCH",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "brief_title": this.cur_brief_title,
                    "brief_url": this.cur_brief_url,
                    "brief_nb_apprs": this.cur_brief_nb_apprs
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
                    this.messages.push(`Brief ${result.brief_title} mis à jour avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchBriefs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        },
        async deleteBrief(brief_id, brief_title) {
            if(confirm(`Voulez vous vraiment supprimer ${brief_title} ?`)){
                fetch(`http://127.0.0.1:8000/api/briefs/${brief_id}/`, {
                    method: "DELETE",
                })
                .then( (response) => {
                    this.clearMessages()
                    if (response.status == 204) {
                        this.messages.push(`Brief supprimé avec succès!`)
                        this.msg_class = "succes_msg"
                        this.hide_all()
                        this.fetchBriefs()
                    } else {
                        throw Error(response.statusText);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            }
        },
        async createGroup(brief_id) {
            fetch(`http://127.0.0.1:8000/api/briefs/gen_groups/${brief_id}`, {
                method: "POST",
            })
            .then( (response) => {
                this.clearMessages()
                if (response.status == 200) {
                    this.messages.push(`Groupes créés avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchBriefs()
                } else {
                    throw Error(response.statusText);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        
        },
        show(brief_id) {
            console.log(`Will display appr #${brief_id} update form`)
            this.briefs.forEach(brief => {
                console.log(`f_update_${brief.id}`)
                this.$refs[`f_update_${brief.id}`][0].style.display = 'none'
                if (brief.id == brief_id){
                    this.cur_brief_title = brief.brief_title
                    this.cur_brief_url = brief.brief_url
                    this.cur_brief_nb_apprs = brief.brief_nb_apprs
                }
            });
            this.$refs[`f_update_${brief_id}`][0].style.display = 'block'
        },
    },
    mounted() {
        this.fetchBriefs()
    }
}
</script>

<template>
    <ul :class="msg_class" v-for="message in this.messages">
        <li>{{ message }}</li>
    </ul>
    <p v-if="!briefs">Loading...</p>
    <div v-else>
        <ul v-for="brief in this.briefs">
            <li>{{ brief.brief_title }}
                <!-- <a href="#" @click="createGroup(brief.id)">Créer Groupes</a> |&nbsp; -->
                <a href="#" @click="show(brief.id)">Modifier</a> |&nbsp;
                <a href="#" @click="deleteBrief(brief.id, brief.brief_title)">Supprimer</a>
                <br>
                <form style="display: none;" :ref="'f_update_' + brief.id" @submit.prevent="updateBrief(brief.id)">
                    <label for="title">Title</label>
                    <input name="title" v-model="cur_brief_title">
                    <label for="url">URL</label>
                    <input name="url" v-model="cur_brief_url">
                    <label for="nb_appr">Nombre d'apprenants</label>
                    <input name="nb_appr" v-model="cur_brief_nb_apprs">
                    <button>Mettre à jour</button>
                </form>
            </li>
            <li v-if="(brief.groups.length==0)">
                Les groupes pour ce brief n'ont pas été encore créés
                <a href="#" @click="createGroup(brief.id)">Créer Groupes</a>
            </li>
            <li v-else>
                <ul v-for="group in brief.groups">
                    <li>
                        {{ group.grp_nom }}
                    </li>
                    <li>
                        <ul v-for="appr in group.grp_apprs">
                            <li>
                                {{ appr.appr_prenom }} {{ appr.appr_nom }}
                            </li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
    <h2>Ajouter un brief</h2>
    <form @submit.prevent="addBrief">
        <label for="title">Title</label>
        <input name="title" v-model="new_brief_title">
        <label for="url">URL</label>
        <input name="url" v-model="new_brief_url">
        <label for="nb_appr">Nombre d'apprenants</label>
        <input name="nb_appr" v-model="new_brief_nb_apprs">
        <button>Ajouter</button>
    </form>
</template>

<style>
.err_msg {
    color: red;
}
.succes_msg {
    color: green;
}
ul {
    list-style: none;
}
</style>