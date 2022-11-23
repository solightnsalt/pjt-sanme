var mapContainer = document.getElementById('map'), // 지도를 표시할 div

mapOption = {
  center: new kakao
    .maps
    .LatLng(33.450701, 126.570667), // 지도의 중심좌표
  level: 5 // 지도의 확대 레벨
};

var map = new kakao
.maps
.Map(mapContainer, mapOption); // 지도를 생성합니다

// --------------------------------------------------------------------------------------------------------------------
// 지도 컨트롤
// 일반 지도와 스카이뷰로 지도 타입을 전환할 수 있는 지도타입 컨트롤을 생성합니다
var mapTypeControl = new kakao.maps.MapTypeControl();

// 지도에 컨트롤을 추가해야 지도위에 표시됩니다
// kakao.maps.ControlPosition은 컨트롤이 표시될 위치를 정의하는데 TOPRIGHT는 오른쪽 위를 의미합니다
map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);

// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

// --------------------------------------------------------------------------------------------------------------------


// ---------------------------------------------------------------------------------------------------------

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

// 주소로 좌표를 검색합니다
function getParkLocation(e){
  var addSearch = document.querySelector(`#${e.id}`)
  var parkLat = addSearch.dataset.latId
  var parkLong = addSearch.dataset.longId

  var coords = new kakao.maps.LatLng(parkLat, parkLong)

  // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
  map.setCenter(coords)
}

// ---------------------------------------------------------------------------------------------------------

var markers = []

function locationLoadSuccess(pos) {
// 현재 위치 받아오기
const x = pos.coords.latitude
const y = pos.coords.longitude

  axios({method: 'get', url: `/map/map/${x}/${y}`})
  .then(response => {
        console.log(response.data)
        var parks = response.data.parkJson

        var imageSrc = "/static/images/star.png"; 

        removeMarker();

        // 지도 위에 표시되고 있는 마커를 모두 제거합니다
        function removeMarker() {
          for ( var i = 0; i < markers.length; i++ ) {
              markers[i].setMap(null);
          }   
          markers = [];
        }

        for(let i=0; i < parks.length; i++){
          var data = parks[i]
          displayMarker(data)
      }
        // 지도에 마커를 표시하는 함수입니다    
      function displayMarker(data) { 

        // 마커 이미지의 이미지 크기 입니다
        var imageSize = new kakao.maps.Size(35, 35)
        
        // 마커 이미지를 생성합니다    
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize)

        // 마커 생성
        var marker = new kakao.maps.Marker({
            map: map,
            position: new kakao.maps.LatLng(data.lat, data.long),
            image : markerImage
        })

        markers.push(marker);  // 배열에 생성된 마커를 추가합니다

        var overlay = new kakao.maps.CustomOverlay({
            yAnchor: 1.3,
            position: marker.getPosition()
        })
        
        var content = document.createElement('div')
        content.classList.add('map-overlay-box')
        content.style.cssText = 'background: white; border: 1px solid black';

        var parkName = document.createElement('p')
        parkName.classList.add('map-overlay-park-name')
        parkName.innerHTML =  data.name;

        var parkAddr = document.createElement('p')
        parkAddr.classList.add('map-overlay-park-addr')
        parkAddr.innerHTML =  data.addr;

        var parkDis = document.createElement('p')
        parkDis.classList.add('map-overlay-park-distance')
        parkDis.innerHTML = "내 위치와의 거리: " + data.userDistance;

        var buttonDiv = document.createElement('div')
        buttonDiv.classList.add('map-button-div', 'd-flex')

        var closeBtn = document.createElement('button')
        closeBtn.classList.add('map-close-btn')
        closeBtn.innerHTML = '닫기'
        closeBtn.onclick = function () {
            overlay.setMap(null)
        }

        var mapform = document.createElement('form')
        mapform.classList.add('map-form')
        mapform.setAttribute('method', 'GET')
        mapform.setAttribute('action', '/create')


        var linkBtn = document.createElement('button')
        linkBtn.classList.add('map-link-btn')
        linkBtn.setAttribute('name', 'park')
        linkBtn.setAttribute('value', `${data.id}`)
        linkBtn.innerHTML = "이 공원에서 산책하기"

        buttonDiv.append(closeBtn, mapform)
        mapform.append(linkBtn)
        content.append(parkName, parkAddr, parkDis, buttonDiv)
        overlay.setContent(content)

        kakao.maps.event.addListener(marker, 'click', function() {
            overlay.setMap(map)
        })
      }
  })


var currentPos = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)

// 지도 이동(기존 위치와 가깝다면 부드럽게 이동)
map.panTo(currentPos);
      
// 마커 생성
var marker = new kakao.maps.Marker({
  position: currentPos,
  image : new kakao.maps.MarkerImage("/static/images/located.png", new kakao.maps.Size(50, 50))
})

// 기존에 마커가 있다면 제거
marker.setMap(null)
marker.setMap(map)
}

function loactionLoadError(pos) {
alert('위치 정보를 가지고 오는데 실패했습니다 ㅜ.ㅜ')
}

// 내 위치 가지고 오기
function getUserLocation() {
navigator.geolocation.getCurrentPosition(locationLoadSuccess, loactionLoadError)
}


// 검색해서 공원 정보 가지고 오기
const mapSearchForm = document.querySelector("#map-search-form")
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

mapSearchForm
.addEventListener('submit', function (event) {

  event.preventDefault()

  function success({ coords, timestamp }) {
    const latitude = coords.latitude;   // 위도
    const longitude = coords.longitude; // 경도

    var currentPos = new kakao.maps.LatLng(latitude, longitude)

    // 지도 이동(기존 위치와 가깝다면 부드럽게 이동)
    map.panTo(currentPos);
          
    // 마커 생성
    var marker = new kakao.maps.Marker({
      position: currentPos,
      image : new kakao.maps.MarkerImage("/static/images/located.png", new kakao.maps.Size(50, 50))
    })

      axios({
        method: 'post',
        url: `/map/map/search/${latitude}/${longitude}/`,
        headers: {
          'X-CSRFToken': csrftoken
        },
        data: new FormData(mapSearchForm)
      }).then(response => {
        const mapSearchResult = document.querySelector("#map-search-result")
        mapSearchResult.textContent = ""
        const parks = response.data.parkJson
    
        if (parks.length === 0) {
          mapSearchResult.insertAdjacentHTML('beforeend', `
        <div class="map-search-result-detail">
          <p>결과를 찾을 수 없습니다</p>
        </div>
        `)
        } else {
    
          var imageSrc = "/static/images/star.png"; 
    
          removeMarker();
    
          // 지도 위에 표시되고 있는 마커를 모두 제거합니다
          function removeMarker() {
            for ( var i = 0; i < markers.length; i++ ) {
                markers[i].setMap(null);
            }   
            markers = [];
          }
    
          for (let i = 0; i < parks.length; i++) {
            var data = parks[i]
            displayMarker(data)
    
            mapSearchResult.insertAdjacentHTML('beforeend', `
            <div class="map-search-result-detail my-3">
              <p class="mb-0 fs-4">공원 이름: ${parks[i].name}</p>
              <p class="mb-0 fs-4">공원 주소: ${parks[i].addr}</p>
              <p class="mb-0 fs-4">내 위치에서의 거리: ${parks[i].userDistance}</p>
              <button type="button" onclick="getParkLocation(this)" class="btn pos-btn mb-4" id="getParkPositionBtn-${i}" data-lat-id=${parks[i].lat} data-long-id=${parks[i].long}>공원 위치 보기</button>
            </div>
          `)
    
            // 지도에 마커를 표시하는 함수입니다    
          function displayMarker(data) { 
    
            // 마커 이미지의 이미지 크기 입니다
            var imageSize = new kakao.maps.Size(35, 35)
            
            // 마커 이미지를 생성합니다
            var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize)
    
            // 마커 생성
            var marker = new kakao.maps.Marker({
                map: map,
                position: new kakao.maps.LatLng(data.lat, data.long),
                image : markerImage
            })
    
            markers.push(marker)
    
            var overlay = new kakao.maps.CustomOverlay({
                yAnchor: 1.3,
                position: marker.getPosition()
            })
            
            var content = document.createElement('div')
            content.classList.add('map-overlay-box')
            content.style.cssText = 'background: white; border: 1px solid black';
    
            var parkName = document.createElement('p')
            parkName.classList.add('map-overlay-park-name')
            parkName.innerHTML =  data.name;
    
            var parkAddr = document.createElement('p')
            parkAddr.classList.add('map-overlay-park-addr')
            parkAddr.innerHTML =  data.addr;
    
            var parkDis = document.createElement('p')
            parkDis.classList.add('map-overlay-park-distance')
            parkDis.innerHTML = "내 위치와의 거리: " + data.userDistance;
    
            var buttonDiv = document.createElement('div')
            buttonDiv.classList.add('map-button-div', 'd-flex')
    
            var closeBtn = document.createElement('button')
            closeBtn.classList.add('map-close-btn')
            closeBtn.innerHTML = '닫기'
            closeBtn.onclick = function () {
                overlay.setMap(null)
            };
    
            var mapform = document.createElement('form')
            mapform.classList.add('map-form')
            mapform.setAttribute('method', 'GET')
            mapform.setAttribute('action', '/create')
    
            var linkBtn = document.createElement('button')
            linkBtn.classList.add('map-link-btn')
            linkBtn.setAttribute('name', 'park')
            linkBtn.setAttribute('value', `${data.id}`)
            linkBtn.innerHTML = "이 공원에서 산책하기"
    
            buttonDiv.append(closeBtn, mapform)
            mapform.append(linkBtn)
            content.append(parkName, parkAddr, parkDis, buttonDiv)
            overlay.setContent(content)
    
            kakao.maps.event.addListener(marker, 'click', function() {
                overlay.setMap(map)
            })
          }
          }
        }
      })
  }

  function getUserLocation() {
      if (!navigator.geolocation) {
          throw "위치 정보가 지원되지 않습니다.";
      }
      navigator.geolocation.getCurrentPosition(success);
  }

  getUserLocation();
})