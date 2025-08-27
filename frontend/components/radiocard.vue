<template>
  <div id="radioCard" class="grid md:grid-cols-5 gap-4 mt-12">
    
    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_World_Service.png" 
        alt="BBC World Service logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_world_service', 'BBC World Service', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC World Service'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20">
          <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/>
        </svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC World Service'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/>
        </svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/LBC_News.png" 
        alt="LBC_News logo" 
        @click="onPlayStream('https://media-ice.musicradio.com/LBC1152', 'LBC_News', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'LBC_News'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'LBC_News'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/LBC_London.png" 
        alt="LBC_London logo" 
        @click="onPlayStream('https://media-ssl.musicradio.com/LBCLondon', 'LBC_London', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'LBC_London'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'LBC_London'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_FM.png" 
        alt="Classical_FM logo" 
        @click="onPlayStream('https://media-the.musicradio.com/ClassicFM', 'Classical FM', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Classical FM'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Classical FM'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>
    
    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/TIMES_Radio.png" 
        alt="TIMES_Radio logo" 
        @click="onPlayStream('https://timesradio.wireless.radio/stream', 'Times Radio', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Times Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Times Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Gold.jpg" 
        alt="Gold logo" 
        @click="onPlayStream('https://media-ssl.musicradio.com/Gold', 'Gold', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Gold'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Gold'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_1.png" 
        alt="BBC_Radio_1 logo" 
        @click="onPlayStream('https://lstn.lv/bbcradio.m3u8?station=bbc_radio_one', 'BBC Radio 1', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio 1'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio 1'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_2.png" 
        alt="BBC_Radio_2 logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_radio_two', 'BBC Radio 2', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio 2'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio 2'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_3.png" 
        alt="BBC_Radio_3 logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_radio_three', 'BBC Radio 3', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio 3'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio 3'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_4.png" 
        alt="BBC_Radio_4 logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm', 'BBC Radio 4', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio 4'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio 4'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_5.png" 
        alt="BBC_Radio_5 logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_radio_five_live', 'BBC Radio 5 Live', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio 5 Live'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio 5 Live'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_Hits_1000.jpg" 
        alt="Classical_Hits_1000 logo" 
        @click="onPlayStream('http://media-ssl.musicradio.com/ClassicalHits', 'Classical Hits', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Classical Hits'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Classical Hits'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_Mozart.jpg" 
        alt="Classical_Mozart logo" 
        @click="onPlayStream('http://media-ssl.musicradio.com/ClassicalMozart', 'Classical Mozart', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Classical Mozart'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Classical Mozart'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/SKY_News.png" 
        alt="SKY_News logo" 
        @click="onPlayStream('https://sky-live.hls.adaptive.skynews.com/hls/live/2012487/skynews/skynews.m3u8', 'Sky News', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Sky News'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Sky News'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/TIMES_Radio.png" 
        alt="TIMES_Radio logo" 
        @click="onPlayStream('http://media-ssl.musicradio.com/TimesRadio', 'Times Radio', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Times Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Times Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_Wales.png" 
        alt="BBC_Radio_Wales logo" 
        @click="onPlayStream('https://stream.live.vc.bbcmedia.co.uk/bbc_radio_wales_fm', 'BBC Radio Wales', 'Live Radio')"
        class="mx-auto h-32 w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio Wales'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio Wales'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

  </div>
</template>

<script setup>
// 1. Define the props this component accepts from its parent.
// This allows the parent to control the loading/playing overlays.
defineProps({
  loadingStreamTitle: {
    type: String,
    default: null
  },
  isPlayingLiveStream: {
    type: Boolean,
    default: false
  },
  currentStreamInfo: {
    type: Object,
    default: null
  }
});

// 2. Define the custom event this component can emit to the parent.
const emit = defineEmits(['play-stream']);

// 3. Create a local method that is called on click.
// This method gathers the station's data and emits the 'play-stream' event.
const onPlayStream = (url, title, artist) => {
  emit('play-stream', { url, title, artist });
};
</script>