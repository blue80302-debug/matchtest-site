/* matchtest.site — nav.js v2
   Dropdown category navigation + mobile hamburger.
   Include via <script src="nav.js"></script> at end of <body>. */
(function(){
    var path = location.pathname;
    var page = path.substring(path.lastIndexOf('/') + 1) || 'index.html';

    var categories = [
        {
            label: '궁합 테스트', key: 'catCompat',
            items: [
                {href:'index.html',      icon:'💕', key:'tabName',  ko:'이름궁합'},
                {href:'mbti.html',        icon:'💜', key:'tabMbti',  ko:'MBTI 궁합'},
                {href:'birthday.html',    icon:'🎂', key:'tabBday',  ko:'생일궁합'},
                {href:'blood-type.html',  icon:'🩸', key:'tabBlood', ko:'혈액형궁합'}
            ]
        },
        {
            label: '성격 테스트', key: 'catPersonality',
            items: [
                {href:'mbti-test.html',   icon:'🧠', key:'tabMbtiTest', ko:'MBTI 검사'},
                {href:'job-test.html',    icon:'💼', key:'tabJob',      ko:'직업적성'},
                {href:'color-test.html',  icon:'🎨', key:'tabColor',    ko:'색깔심리'}
            ]
        },
        {
            label: '재미 테스트', key: 'catFun',
            items: [
                {href:'pet-name.html',    icon:'🐾', key:'tabPet',     ko:'펫 작명소'},
                {href:'past-life.html',   icon:'🔮', key:'tabPast',    ko:'전생테스트'},
                {href:'fortune.html',     icon:'⭐',        key:'tabFortune', ko:'오늘의 운세'}
            ]
        }
    ];

    var activeCatIdx = -1;
    categories.forEach(function(cat, ci){
        cat.items.forEach(function(item){
            if(item.href === page) activeCatIdx = ci;
        });
    });

    /* ── Desktop nav ── */
    var html = '<nav class="nav-bar" id="navBar">';
    html += '<a href="index.html" class="nav-logo">💕 MatchTest</a>';
    html += '<div class="nav-menu">';
    categories.forEach(function(cat, ci){
        var catActive = (ci === activeCatIdx) ? ' nav-category--active' : '';
        html += '<div class="nav-category-wrap">';
        html += '<button class="nav-category' + catActive + '" data-cat="' + ci + '">'
              + '<span class="tab-text" data-key="' + cat.key + '">' + cat.label + '</span>'
              + ' <span class="nav-arrow">▾</span></button>';
        html += '<div class="nav-dropdown">';
        cat.items.forEach(function(item){
            var cls = (item.href === page) ? ' class="active"' : '';
            html += '<a href="' + item.href + '"' + cls + '>'
                  + '<span class="nav-item-icon">' + item.icon + '</span>'
                  + ' <span class="tab-text" data-key="' + item.key + '">' + item.ko + '</span></a>';
        });
        html += '</div></div>';
    });
    html += '</div>';

    /* Hamburger button */
    html += '<button class="nav-hamburger" id="navHamburger" aria-label="Menu">'
          + '<span></span><span></span><span></span></button>';
    html += '</nav>';

    /* ── Mobile overlay ── */
    html += '<div class="nav-overlay" id="navOverlay">';
    html += '<div class="nav-overlay-header">';
    html += '<a href="index.html" class="nav-logo">💕 MatchTest</a>';
    html += '<button class="nav-overlay-close" id="navClose" aria-label="Close">✕</button>';
    html += '</div>';
    html += '<div class="nav-overlay-body">';
    categories.forEach(function(cat, ci){
        var open = (ci === activeCatIdx) ? ' nav-accordion--open' : '';
        html += '<div class="nav-accordion' + open + '">';
        html += '<button class="nav-accordion-btn" data-acc="' + ci + '">'
              + '<span class="tab-text" data-key="' + cat.key + '">' + cat.label + '</span>'
              + ' <span class="nav-acc-arrow">▾</span></button>';
        html += '<div class="nav-accordion-panel">';
        cat.items.forEach(function(item){
            var cls = (item.href === page) ? ' class="active"' : '';
            html += '<a href="' + item.href + '"' + cls + '>'
                  + '<span class="nav-item-icon">' + item.icon + '</span>'
                  + ' <span class="tab-text" data-key="' + item.key + '">' + item.ko + '</span></a>';
        });
        html += '</div></div>';
    });
    html += '</div></div>';

    /* ── Inject ── */
    var target = document.getElementById('nav-placeholder');
    if(target){
        target.outerHTML = html;
    } else {
        document.body.insertAdjacentHTML('afterbegin', html);
    }

    /* ── Event handlers ── */
    var hamburger = document.getElementById('navHamburger');
    var overlay = document.getElementById('navOverlay');
    var closeBtn = document.getElementById('navClose');

    hamburger.addEventListener('click', function(){
        overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    });

    function closeOverlay(){
        overlay.classList.remove('open');
        document.body.style.overflow = '';
    }
    closeBtn.addEventListener('click', closeOverlay);
    overlay.addEventListener('click', function(e){
        if(e.target === overlay) closeOverlay();
    });

    /* Mobile accordion toggle */
    var accBtns = document.querySelectorAll('.nav-accordion-btn');
    for(var i = 0; i < accBtns.length; i++){
        accBtns[i].addEventListener('click', function(){
            this.parentElement.classList.toggle('nav-accordion--open');
        });
    }

    /* Desktop: close dropdowns when clicking outside */
    document.addEventListener('click', function(e){
        if(!e.target.closest('.nav-category-wrap')){
            var opens = document.querySelectorAll('.nav-category-wrap.open');
            for(var j = 0; j < opens.length; j++) opens[j].classList.remove('open');
        }
    });

    /* Desktop category buttons: toggle on click (for touch desktops) */
    var catBtns = document.querySelectorAll('.nav-category');
    for(var k = 0; k < catBtns.length; k++){
        catBtns[k].addEventListener('click', function(e){
            e.stopPropagation();
            var wrap = this.parentElement;
            var wasOpen = wrap.classList.contains('open');
            var allWraps = document.querySelectorAll('.nav-category-wrap.open');
            for(var m = 0; m < allWraps.length; m++) allWraps[m].classList.remove('open');
            if(!wasOpen) wrap.classList.add('open');
        });
    }
})();
