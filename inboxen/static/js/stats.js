/*!
 * Copyright (c) 2016 Jessica Tallon & Matt Molyneaux
 * Licensed under AGPLv3 (https://github.com/Inboxen/Inboxen/blob/master/LICENSE)
 */

(function($, Chart) {
    'use strict';

    var statsUrl, $userCanvas, $inboxCanvas, $emailCanvas;
    statsUrl = $("#stats-chart").data("url");
    $userCanvas = $("<canvas></canvas>");
    $inboxCanvas = $("<canvas></canvas>");
    $emailCanvas = $("<canvas></canvas>");

    // override some defaults
    Chart.defaults.global.responsive = true;
    Chart.defaults.global.maintainAspectRatio = false;
    Chart.defaults.global.animation = false;
    Chart.defaults.global.scaleBeginAtZero = true;
    Chart.defaults.global.showTooltips = false;
    Chart.defaults.global.bezierCurve = false;

    // hack to bypass evil "new Function"
    Chart.defaults.global.tooltipTitleTemplate = function(obj) {
        return obj.label;
    };
    Chart.defaults.global.tooltipTemplate = function(obj) {
        var out = ""
        if (obj.label) {
            out = out + obj.label + ": ";
        }
        out = out + obj.value;
        return out
    };
    Chart.defaults.global.multiTooltipTemplate = function(obj) {
        return obj.value;
    };
    Chart.defaults.global.scaleLabel = function(obj) {
        return obj.value;
    };

    $.get(statsUrl, function(data) {
        var userChart, inboxChart, emailChart, fakeLabels;
        var userLineChart, inboxLineChart, emailLineChart;

        // horrible hack to avoid printing the full dates under the X axis
        fakeLabels = new Array(data.dates.length);
        for (var i = 0; i < data.dates.length; i++) {
            fakeLabels[i] = "";
        }

        // colours picked here: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Colors/Color_picker_tool
        // picked a nice red, and then pick two more colours 120 deg hue above and below to get the blue and green

        $("#users-chart").prepend($userCanvas);
        userChart = new Chart($userCanvas[0].getContext("2d"));
        userChart.Line({
            labels: fakeLabels,
            datasets: [{
                label: "Users",
                fillColor: "rgba(191, 63, 95, 0.5)",
                strokeColor: "rgb(191, 63, 95)",
                pointStrokeColor: "rgb(191, 63, 95)",
                pointHighlightFill: "rgb(191, 63, 95)",
                pointHighlightStroke: "rgb(191, 63, 95)",
                data: data.users
            }]
        },
        {
            pointDot: false,
            scaleShowVerticalLines: false
        });

        $("#inboxes-chart").prepend($inboxCanvas);
        inboxChart = new Chart($inboxCanvas[0].getContext("2d"));
        inboxChart.Line({
            labels: fakeLabels,
            datasets: [{
                label: "Inboxes",
                fillColor: "rgba(95, 191, 63, 0.5)",
                strokeColor: "rgb(95, 191, 63)",
                pointStrokeColor: "rgb(95, 191, 63)",
                pointHighlightFill: "rgb(95, 191, 63)",
                pointHighlightStroke: "rgb(95, 191, 63)",
                data: data.inboxes
            }]
        },{
            pointDot: false,
            scaleShowVerticalLines: false
        });

        $("#emails-chart").prepend($emailCanvas);
        emailChart = new Chart($emailCanvas[0].getContext("2d"));
        emailChart.Line({
            labels: fakeLabels,
            datasets: [{
                label: "Emails",
                fillColor: "rgba(63, 95, 191, 0.5)",
                strokeColor: "rgb(63, 95, 191)",
                pointStrokeColor: "rgb(63, 95, 191)",
                pointHighlightFill: "rgb(63, 95, 191)",
                pointHighlightStroke: "rgb(63, 95, 191)",
                data: data.emails
            }]
        },{
            pointDot: false,
            scaleShowVerticalLines: false
        });
    });
})(jQuery, Chart);
