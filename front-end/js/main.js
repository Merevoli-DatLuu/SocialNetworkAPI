Vue.component('person-chat', {
    template: `
    <a @click="focusMessage()">
        <div class="media-left">
            <img class="img-circle img-xs" src="img/profile-photos/1.png"
                alt="Profile Picture">
            <i class="
            badge badge-info badge-stat badge-icon
            pull-left
            "></i>
        </div>
        <div class="media-body">
            <span class="chat-info pull-right">
                <span class="text-xs">{{time}}</span>
                <span class="badge badge-success">1</span>
            </span>
            <div class="chat-text">
                <p class="chat-username"><b>{{name}}</b></p>
                <p style="font-size: 12px;">{{message}}</p>
            </div>
        </div>
    </a>
    `,
    methods: {
        focusMessage: function () {
            this.$emit('openmessagepanel', this.message_id, this.name, this.message_type)
        }
    },
    props: {
        avatar: String,
        message_id: Number,
        message_type: String,
        name: String,
        message: String,
        time: String,
        persons: Array,
    }
});


Vue.component('message-list', {
    data: function () {
        return {
            persons: [],
            groups: []
        }
    },
    template: `
    <div class="chat-user-list">
            <p class="header_chat"> Private Messages </p>
            <person-chat
                v-for="person in persons"
                :key="person.id"
                :message_id="person.message_id"
                :message_type="person.message_type"
                :avatar="person.avatar"
                :name="person.name"
                :message="person.message"
                :time="person.time"
                :persons="persons"
                @openmessagepanel="openMessagePanel"
            />
            <p class="header_chat"> Group Messages </p>
            <person-chat
                v-for="group in groups"
                :key="group.id"
                :message_id="group.message_id"
                :message_type="group.message_type"
                :avatar="group.avatar"
                :name="group.name"
                :message="group.message"
                :time="group.time"
                :persons="groups"
                @openmessagepanel="openMessagePanel"
            />
    </div>`,
    created: function () {
        var access_token = localStorage.getItem('access_token')
        const request = (() => axios.get('http://127.0.0.1:8000/api/v1/message/', {
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {

            data = response.data.results
            console.log(data)
            persons = []
            for (let i = 0; i < data.length; i++) {
                var name = data[i].user_name
                if (localStorage.getItem('cuser') == data[i].user_id) {
                    name = "Me"
                }

                persons.push({
                    id: data[i].user_id,
                    message_id: data[i].id,
                    message_type: "private",
                    avatar: "Default",
                    name: name,
                    message: data[i].last_message,
                    time: this.formatTime(data[i].updated_time)
                })
            }
            this.persons.push(...persons)

        })
        .catch(e => console.log(e)))

        const request_group = (() => axios.get('http://127.0.0.1:8000/api/v1/message/group/joined', {
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {

            data = response.data.results
            console.log(data)
            groups = []
            for (let i = 0; i < data.length; i++) {
                groups.push({
                    id: data[i].id,
                    message_id: data[i].id,
                    message_type: "group",
                    avatar: "Default",
                    name: data[i].name,
                    message: data[i].last_message,
                    time: this.formatTime(data[i].updated_time)
                })
            }
            this.groups.push(...groups)

        })
        .catch(e => console.log(e)))

        request()
        request_group()
    },
    methods: {
        formatTime: function (datetime) {
            date = new Date(datetime)
            time = (Date.now() - date) / 1000
            days = time / (3600 * 24)

            if (days < 1) {
                if (time < 60){
                    return `${parseInt(time)} second(s) ago`
                }
                else if (time < 60*60){
                    return `${parseInt(time/60)} minute(s) ago`
                }
                else {
                    return `${parseInt(time/3600)} hour(s) ago`
                }
            }
            else {
                if (days < 7) {
                    return `${parseInt(days)} day(s) ago`
                }
                else {
                    weeks = days / 7
                    return `${parseInt(weeks)} week(s) ago`

                }
            }
        },
        openMessagePanel: function (message_id, name, message_type) {
            this.$emit('openmessagepanel', message_id, name, message_type)
        }
    }
})


Vue.component('message-sidebar', {
    data: function () {
        return {
            search_input: ""
        }
    },
    template: `
    <div class="page-fixedbar-container">
        <div class="page-fixedbar-content">
            <div class="nano">
                <div class="nano-content">
                    <div class="pad-all bord-btm">
                        <input type="text" placeholder="Search or start new chat" class="form-control">
                    </div>
                    <message-list
                        @openmessagepanel="openMessagePanel"
                    />
                </div>
            </div>
        </div>
    </div>`,
    methods: {
        openMessagePanel: function (message_id, name, message_type) {
            this.$emit('openmessagepanel', message_id, name, message_type)
        }
    }
})


Vue.component('message-chat', {
    template: `
    <div v-if="is_owner == true" class="chat-me">
        <div v-bind:data-tooltip-avatar=avatar class="media-left">
            <img src="img/profile-photos/1.png" class="img-circle img-sm" alt="Profile Picture">
        </div>
        <div class="media-body">
            <div v-for="content in contents">
                <p v-bind:data-tooltip=content.time>{{content.message}}
                    <!--small>{{content.time}}</small-->
                </p>
            </div>
        </div>
    </div>
    <div v-else class="chat-user">
        <div v-bind:data-tooltip-avatar=avatar class="media-left">
            <img src="img/profile-photos/1.png" class="img-circle img-sm" alt="Profile Picture">
        </div>
        <div class="media-body">
            <div v-for="content in contents">
                <p v-bind:data-tooltip-right=content.time>{{content.message}}
                    <!--small>{{contents.time}}</small-->
                </p>
            </div>
        </div>
    </div>`,
    props: {
        avatar: String,
        is_owner: Boolean,
        contents: Array,
        message_contents: Array
    }
})


Vue.component('message-content', {
    data: function () {
        return {
            first_render: true,
        }
    },
    template: `
    <div class="nano" style="height: 60vh">
        <div style="padding: 10px;" v-if="is_loading"> loading... </div>
        <div id="nano-content-full" class="nano-content" style="background-color:#D6DBE0; height: inherit;">
            <div class="panel-body chat-body media-block">
                <message-chat
                v-for="message in message_contents"
                :avatar="message.avatar"
                :is_owner="message.is_owner"
                :contents="message.contents"
                :message_contents="message_contents"
                ></message-chat>
            </div>
        </div>
    </div>`,
    updated: function (){
        if (!this.is_loading) {
            scroll_obj = $("#scroll-chat")[0]
            scroll_obj.scrollTop = scroll_obj.scrollHeight
        }

        if (this.first_render){
            scroll_obj.addEventListener("scroll", () => {
                if (!this.is_loading && scroll_obj.scrollTop == 0 && this.next_message) { 
                    console.log(100)
                    this.$emit('loading_next_message')
                }
            })
            this.first_render = false
        }
    },
    props: {
        message_contents: Array,
        next_message: String,
        is_loading: Boolean,
    }
})


Vue.component('message-send', {
    data: function () {
        return { message_input: "" }
    },
    template: `
    <div class="pad-all">
        <div class="input-group">
            <input v-model="message_input" @keydown.enter="sendMessage" type="text" placeholder="Type your message" class="form-control form-control-trans">
            <span class="input-group-btn">
                <button class="btn btn-icon add-tooltip" data-original-title="Add file"
                    type="button">
                    <i class="demo-psi-paperclip icon-lg"></i>
                </button>
                <button class="btn btn-icon add-tooltip" data-original-title="Emoticons"
                    type="button">
                    <i class="demo-pli-smile icon-lg"></i>
                </button>
                <button class="btn btn-icon add-tooltip" data-original-title="Send" type="button" @click="sendMessage">
                    <i class="demo-pli-paper-plane icon-lg"></i>
                </button>
            </span>
        </div>
    </div>`,
    methods: {
        sendMessage: function () {
            if (this.message_input != "") {
                this.$emit('sendmessagesocket', this.message_input);
                this.message_input = ""
            }
        }
    },
    props: {
        message_contents: Array,
    }
})


Vue.component('message-header', {
    template: `
    <div class="media-block pad-all bord-btm">
        <div class="pull-right">
            <div class="btn-group dropdown">
                <a href="#" class="dropdown-toggle btn btn-trans" data-toggle="dropdown" aria-expanded="false">
                    <i class="pci-ver-dots">
                    </i>
                </a>
                <ul class="dropdown-menu dropdown-menu-right" style="">
                    <li>
                        <a href="#">
                            <i class="icon-lg icon-fw demo-psi-pen-5"></i> Edit
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <i class="icon-lg icon-fw demo-pli-recycling"></i> Remove
                        </a>
                    </li>
                    <li class="divider"></li>
                    <li>
                        <a href="#">
                            <i class="icon-lg icon-fw demo-pli-mail"></i> Send a Message
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <i class="icon-lg icon-fw demo-pli-calendar-4"></i> View Details
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <i class="icon-lg icon-fw demo-pli-lock-user"></i> Lock
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="media-left">
            <img class="img-circle img-xs" src="img/profile-photos/1.png" alt="Profile Picture">
        </div>
        <div class="media-body">
            <p class="mar-no text-main text-bold text-lg">{{name}}</p>
            <small class="text-muteds">Typing....</small>
        </div>
    </div>`,
    props: {
        name: String
    }
})


Vue.component('message-panel', {
    template: `
    <div id="page-content">
        <div class="panel">
            <message-header :name="name"/>
            <message-content 
                :message_contents="message_contents"
                :next_message="next_message"
                :is_loading="is_loading"
                @loading_next_message="loading_next_message"
            />
            <message-send 
                :message_contents="message_contents"
                @sendmessagesocket="send"
            />
        </div>
    </div>`,
    props: {
        name: String,
        message_contents: Array,
        next_message: String,
        is_loading: Boolean,
    },
    methods: {
        send: function (message) {
            this.$emit('sendmessagesocket', message)
        },
        loading_next_message: function () {
            this.$emit('loading_next_message')
        }
    }
})


let vm = new Vue({
    el: '#app',
    data: function () {
        return {
            name: "",
            message_contents: [],
            connection: "",
            is_loading: false,
            next_message: null,
            is_update_next_message: false,
            scrollh_1: 0,
            scrollh_2: 0
        }
    },
    template: `
    <div class="boxed">
        <div id="content-container">
            <div id="page-head"></div>
            <div>
                <message-sidebar
                    @openmessagepanel="initMessage"
                />
                <message-panel 
                    :name="name"
                    :message_contents="message_contents"
                    :next_message="next_message"
                    :is_loading="is_loading"
                    @sendmessagesocket="sendMessageSocket"
                    @loading_next_message="loading_next_message"
                />
            </div>
        </div>
    </div>`,
    created: function () {
        this.cuser = localStorage.getItem("cuser")
    },
    updated: function () {
        if (this.is_update_next_message) {
            this.is_update_next_message = false
            scroll_obj = $("#scroll-chat")[0]
            this.scrollh_2 = scroll_obj.scrollHeight
            console.log(this.scrollh_2)
            console.log(this.scrollh_1)
            scroll_obj.scrollTop = this.scrollh_2 - this.scrollh_1
        } 
    },
    methods: {
        createMessageSocket: function (message_id, message_type) {

            if (this.connection != ""){
                console.log(this.connection)
                this.connection.close()
            }

            var connectionString;
            if (message_type == 'private'){
                connectionString = `ws://localhost:8000/ws/message/${message_id}?token=${localStorage.getItem('access_token')}`;
            }
            else if (message_type == 'group'){  
                connectionString = `ws://localhost:8000/ws/message/group/${message_id}?token=${localStorage.getItem('access_token')}`;
            }
            this.connection = new WebSocket(connectionString)
    
            this.connection.onmessage = this.onMessage
    
            this.connection.onopen = function (event) {
                console.log(event)
                console.log("Successfully connected to the echo websocket server...")
            }

        },
        sendMessageSocket: function (message) {
            console.log("sending " + message)
            this.connection.send(JSON.stringify({
                message: message
            }));
        },
        initMessage: function (message_id, name, message_type) {
            var request;
            this.createMessageSocket(message_id, message_type);
            if (message_type == 'private') {
                request = (() => axios.get(`http://127.0.0.1:8000/api/v1/message/${message_id}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {

                    data = response.data.results
                    console.log(data)
                    messages = []
                    for (let i = 0; i < data.length; i++) {
                        console.log(messages.length == 0)
                        if (messages.length == 0 || messages[0].is_owner != (data[i].user_id == this.cuser)) {
                            messages.unshift({
                                avatar: data[i].user_name,
                                is_owner: data[i].user_id == this.cuser,
                                contents: [{
                                    message: data[i].content,
                                    time: this.formatDatetime(data[i].created_time)
                                }]
                            })
                        }
                        else {
                            messages[0].contents.unshift({
                                message: data[i].content,
                                time: this.formatDatetime(data[i].created_time)
                            })
                        }
                    }
                    console.log(messages)
                    this.message_contents = messages
                    this.next_message = response.data.next
                })
                .catch(e => console.log(e)))
            }
            else if (message_type == 'group') {
                request = (() => axios.get(`http://127.0.0.1:8000/api/v1/message/group/${message_id}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {

                    data = response.data.results
                    console.log(data)
                    messages = []
                    for (let i = 0; i < data.length; i++) {
                        console.log(messages.length == 0)
                        if (messages.length == 0 || messages[0].is_owner != (data[i].user_id == this.cuser)) {
                            messages.unshift({
                                avatar: data[i].user_name,
                                is_owner: data[i].user_id == this.cuser,
                                contents: [{
                                    message: data[i].content,
                                    time: this.formatDatetime(data[i].created_time)
                                }]
                            })
                        }
                        else {
                            messages[0].contents.unshift({
                                message: data[i].content,
                                time: this.formatDatetime(data[i].created_time)
                            })
                        }
                    }
                    console.log(messages)
                    this.message_contents = messages
                    this.next_message = response.data.next
                })
                .catch(e => console.log(e)))
            }

            this.message_id = message_id
            this.message_type = message_type
            this.name = name
            request()

        },
        loading_next_message: function () {
            this.is_loading = true
            axios.get(this.next_message, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                data = response.data.results
                console.log(data)
                messages = []
                for (let i = 0; i < data.length; i++) {
                    console.log(messages.length == 0)
                    if (messages.length == 0 || messages[0].is_owner != (data[i].user_id == this.cuser)) {
                        messages.unshift({
                            avatar: data[i].user_name,
                            is_owner: data[i].user_id == this.cuser,
                            contents: [{
                                message: data[i].content,
                                time: this.formatDatetime(data[i].created_time)
                            }]
                        })
                    }
                    else {
                        messages[0].contents.unshift({
                            message: data[i].content,
                            time: this.formatDatetime(data[i].created_time)
                        })
                    }
                }
                console.log(messages)
                
                scroll_obj = $("#scroll-chat")[0]
                this.scrollh_1 = scroll_obj.scrollHeight
                this.message_contents.unshift(...messages)
                this.next_message = response.data.next
                this.is_loading = false
                this.is_update_next_message = true
            })
            .catch(e => console.log(e))
        },
        formatDatetime: function (datetime) {
            var date = new Date(datetime)
            var time = (Date.now() - date) / 1000
            var days = time / (3600 * 24)

            memoDate = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

            if (days < 1) {
                var hours = ("0" + date.getHours()).slice(-2);
                var minutes = ("0" + date.getMinutes()).slice(-2);
                return `${hours}:${minutes}`
            }
            else if (days < 7){
                let day = memoDate[date.getDate()]
                var hours = ("0" + date.getHours()).slice(-2);
                var minutes = ("0" + date.getMinutes()).slice(-2);
                return `${day} at ${hours}:${minutes}`
            }
            else {
                let fulldate = date.getDate() + '-' +(date.getMonth()+1) + '-' + date.getFullYear()
                var hours = ("0" + date.getHours()).slice(-2);
                var minutes = ("0" + date.getMinutes()).slice(-2);
                return `${fulldate} at ${hours}:${minutes}`
            }
        },
        onMessage: function (event) {
            data = JSON.parse(event.data)
            console.log(data);
            console.log(this.message_contents);
            let last_messsage = this.message_contents[this.message_contents.length - 1]
            if (last_messsage.is_owner == (data.payload.user_id == data.payload.cuser)) {
                this.message_contents[this.message_contents.length - 1].contents.push({
                    message: data.payload.content,
                    time: this.formatDatetime(data.payload.created_time)
                })
            }
            else {
                this.message_contents.push({
                    avatar: data.payload.user_name,
                    is_owner: (data.payload.user_id == data.payload.cuser),
                    contents: [{
                        message: data.payload.content,
                        time: this.formatDatetime(data.payload.created_time)
                    }]
                })
            }
        }
    },
})


