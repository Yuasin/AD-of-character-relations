//获取数据
fetch('./static/analyseData1.json')
    .then((res) => res.json())
    .then((data) => {

        //人物出现频次环形图
        var frequency_myChart = echarts.init(document.getElementById('frequency'));
        var frequency_option;

        frequency_option = {
            tooltip: {
                trigger: 'item'
            },
            legend: {
                top: '0%',
                left: 'center'
            },
            series: [
                {
                    name: '人物出现次数',
                    type: 'pie',
                    radius: ['50%', '60%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '40',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: true
                    },
                    data: data.frequency
                }
            ]
        };
        frequency_option && frequency_myChart.setOption(frequency_option);

        //网络密度仪表盘
        var density_myChart = echarts.init(document.getElementById('density'));
        var option_density;
        option_density = {
            series: [{
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: 1,
                splitNumber: 8,
                axisLine: {
                    lineStyle: {
                        width: 6,
                        color: [
                            [0.15, '#FF6E76'],
                            [0.30, '#FDDD60'],
                            [0.6, '#58D9F9'],
                            [1, '#7CFFB2']
                        ]
                    }
                },
                pointer: {
                    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    length: '12%',
                    width: 20,
                    offsetCenter: [0, '-60%'],
                    itemStyle: {
                        color: 'auto'
                    }
                },
                axisTick: {
                    length: 12,
                    lineStyle: {
                        color: 'auto',
                        width: 2
                    }
                },
                splitLine: {
                    length: 20,
                    lineStyle: {
                        color: 'auto',
                        width: 5
                    }
                },
                axisLabel: {
                    color: '#464646',
                    fontSize: 20,
                    distance: -60,
                    formatter: function (value) {
                        if (value === 0.750) {
                            return '密';
                        } else if (value === 0.500) {
                            return '高';
                        } else if (value === 0.250) {
                            return '中';
                        } else if (value === 0.125) {
                            return '疏';
                        }
                    }
                },
                title: {
                    offsetCenter: [0, '-20%'],
                    fontSize: 30
                },
                detail: {
                    fontSize: 50,
                    offsetCenter: [0, '0%'],
                    valueAnimation: true,
                    formatter: function (value) {
                        return Math.round(value * 100) + '%';
                    },
                    color: 'auto'
                },
                data: [data.density]
            }]
        };
        option_density && density_myChart.setOption(option_density);


        //三种中心性
        var centrality_myChart = echarts.init(document.getElementById('centrality'));
        var centrality_option;

        centrality_option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true
                    }
                }
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: true,
            legend: {
                data: ['介数中心性', '点度中心性', '接近中心性'],
                itemGap: 1,
                left: "left"
            },
            grid: {
                top: '12%',
                left: '1%',
                right: '10%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: data.centrality.names,
                    position: "top"
                },
                {
                    type: 'category',
                    data: data.centrality.pinyinnames,
                    axisLabel: {
                        show: true,
                        rotate: 40,
                        textStyle: {
                            color: 'blue',
                            fontFamily: 'sans-serif',
                            fontSize: 12,
                            fontStyle: 'italic',
                            fontWeight: 'bold'
                        }
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    axisLabel: {
                        formatter: function (a) {
                            a = +a;
                            return isFinite(a)
                                ? echarts.format.addCommas(+a / 1000)
                                : '';
                        }
                    }
                }
            ],
            dataZoom: [
                {
                    show: true,
                    start: 94,
                    end: 100
                },
                {
                    type: 'inside',
                    start: 94,
                    end: 100
                },
                {
                    show: true,
                    yAxisIndex: 0,
                    filterMode: 'empty',
                    width: 20,
                    height: '80%',
                    showDataShadow: false,
                    left: '93%'
                }
            ],
            series: [
                {
                    name: '介数中心性',
                    type: 'bar',
                    data: data.centrality.between
                },
                {
                    name: '点度中心性',
                    type: 'bar',
                    data: data.centrality.degree
                },
                {
                    name: '接近中心性',
                    type: 'bar',
                    data: data.centrality.closeness
                },
            ]
        };
        centrality_option && centrality_myChart.setOption(centrality_option);

        //点度中心性
        var degree_myChart = echarts.init(document.getElementById('degree'));
        var degree_option;

        degree_option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true
                    }
                }
            },
            xAxis: [{
                type: 'category',
                data: data.degree.name,
                position: "top"
            }, {
                type: 'category',
                data: data.degree.pinyinname,
                axisLabel: {
                    show: true,
                    rotate: 40,
                    textStyle: {
                        color: 'blue',
                        fontFamily: 'sans-serif',
                        fontSize: 10,
                        fontStyle: 'italic',
                        fontWeight: 'bold'
                    }
                }
            }
            ],
            yAxis: {
                type: 'value'
            },
            series: [{
                data: data.degree.data,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }]
        };
        degree_option && degree_myChart.setOption(degree_option);

        //介数中心性
        var between_myChart = echarts.init(document.getElementById('between'));
        var between_option;

        between_option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true
                    }
                }
            },
            xAxis: [{
                type: 'category',
                data: data.between.name,
                position: "top"
            }, {
                type: 'category',
                data: data.between.pinyinname,
                axisLabel: {
                    show: true,
                    rotate: 40,
                    textStyle: {
                        color: 'blue',
                        fontFamily: 'sans-serif',
                        fontSize: 10,
                        fontStyle: 'italic',
                        fontWeight: 'bold'
                    }
                }
            }
            ],
            yAxis: {
                type: 'value'
            },
            series: [{
                data: data.between.data,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }]
        };
        between_option && between_myChart.setOption(between_option);

        //接近中心性
        var closeness_myChart = echarts.init(document.getElementById('closeness'));
        var closeness_option;

        closeness_option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true
                    }
                }
            },
            xAxis: [{
                type: 'category',
                data: data.closeness.name,
                position: "top"
            }, {
                type: 'category',
                data: data.closeness.pinyinname,
                axisLabel: {
                    show: true,
                    rotate: 40,
                    textStyle: {
                        color: 'blue',
                        fontFamily: 'sans-serif',
                        fontSize: 10,
                        fontStyle: 'italic',
                        fontWeight: 'bold'
                    }
                }
            }
            ],
            yAxis: {
                type: 'value'
            },
            series: [{
                data: data.closeness.data,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }]
        };
        closeness_option && closeness_myChart.setOption(closeness_option);


        //聚类系数柱状图
        var cluster_myChart = echarts.init(document.getElementById('cluster'));
        var cluster_option;

        cluster_option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true
                    }
                }
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            xAxis: [{
                type: 'category',
                data: data.cluster.names,
                position: "top"
            }, {
                type: 'category',
                data: data.cluster.pinyinnames,
                axisLabel: {
                    show: true,
                    rotate: 40,
                    textStyle: {
                        color: 'blue',
                        fontFamily: 'sans-serif',
                        fontSize: 10,
                        fontStyle: 'italic',
                        fontWeight: 'bold'
                    }
                }
            }
            ],
            yAxis: {
                type: 'value',
                max: 1.2
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 94,
                    end: 100
                },
                {
                    show: true,
                    yAxisIndex: 0,
                    filterMode: 'empty',
                    width: 20,
                    height: '80%',
                    showDataShadow: false,
                    left: '93%'
                },
                {
                    show: false,
                    xAxisIndex: 0,
                    filterMode: 'empty',
                    height: 15,
                    top: '96%'
                }
            ],
            series: [{
                data: data.cluster.values,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }]
        };

        cluster_option && cluster_myChart.setOption(cluster_option);

        //网络密度仪表盘
        var average_cluster_myChart = echarts.init(document.getElementById('average-cluster'));
        var average_cluster_option;
        average_cluster_option = {
            series: [{
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: 1,
                splitNumber: 8,
                axisLine: {
                    lineStyle: {
                        width: 6,
                        color: [
                            [0.25, '#FF6E76'],
                            [0.50, '#FDDD60'],
                            [0.75, '#58D9F9'],
                            [1, '#7CFFB2']
                        ]
                    }
                },
                pointer: {
                    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    length: '12%',
                    width: 20,
                    offsetCenter: [0, '-60%'],
                    itemStyle: {
                        color: 'auto'
                    }
                },
                axisTick: {
                    length: 12,
                    lineStyle: {
                        color: 'auto',
                        width: 2
                    }
                },
                splitLine: {
                    length: 20,
                    lineStyle: {
                        color: 'auto',
                        width: 5
                    }
                },
                axisLabel: {
                    color: '#464646',
                    fontSize: 20,
                    distance: -60,
                    formatter: function (value) {
                        if (value === 0.875) {
                            return '高';
                        } else if (value === 0.625) {
                            return '中';
                        } else if (value === 0.375) {
                            return '良';
                        } else if (value === 0.125) {
                            return '低';
                        }
                    }
                },
                title: {
                    offsetCenter: [0, '-20%'],
                    fontSize: 30
                },
                detail: {
                    fontSize: 50,
                    offsetCenter: [0, '0%'],
                    valueAnimation: true,
                    formatter: function (value) {
                        return Math.round(value * 100) + '%';
                    },
                    color: 'auto'
                },
                data: [data.average_cluster]
            }]
        };
        average_cluster_option && average_cluster_myChart.setOption(average_cluster_option);


        // 路径相关
        var path_myChart = echarts.init(document.getElementById('path'));
        var path_option;

        path_option = {
            legend: {
                data: data.path.names
            },
            series: [
                {
                    name: '距离',
                    type: 'pie',
                    selectedMode: 'single',
                    radius: [0, '40%'],
                    label: {
                        position: 'inner',
                        fontSize: 12,
                    },
                    labelLine: {
                        show: true
                    },
                    data: [
                        {value: 10, name: '直径:\n\n' + data.path.dia},
                        {value: 10, name: '平均最短路径:\n\n' + data.path.shortest},
                    ]
                },
                {
                    name: '最短路径统计',
                    type: 'pie',
                    radius: ['45%', '55%'],
                    labelLine: {
                        length: 18,
                    },
                    label: {
                        formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                        backgroundColor: '#F6F8FC',
                        borderColor: '#8C8D8E',
                        borderWidth: 1,
                        borderRadius: 4,

                        rich: {
                            a: {
                                color: '#6E7079',
                                lineHeight: 12,
                                align: 'center'
                            },
                            hr: {
                                borderColor: '#8C8D8E',
                                width: '100%',
                                borderWidth: 1,
                                height: 0
                            },
                            b: {
                                color: '#4C5058',
                                fontSize: 10,
                                fontWeight: 'bold',
                                lineHeight: 14
                            },
                            per: {
                                color: '#fff',
                                backgroundColor: '#4C5058',
                                padding: [3, 4],
                                borderRadius: 4
                            }
                        }
                    },
                    data: data.path.dis
                }
            ]
        };

        path_option && path_myChart.setOption(path_option);
    });