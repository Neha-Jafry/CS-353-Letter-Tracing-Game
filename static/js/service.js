var boxServices = angular.module('boxServices', ['ngResource']);

boxServices.factory('MachineService', ['$resource',
  function($resource){
    return   $resource('http://127.0.0.1:5000/game/score',
        {query: {method:'GET', params: {}, isArray:false}
    });
}]);