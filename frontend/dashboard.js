document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard script loaded');
    
    // DOM Elements
    const viewButtons = document.querySelectorAll('.view-btn');
    const dashboardContent = document.getElementById('dashboard-content');
    const dateRangeFilter = document.getElementById('date-range');
    const assignmentTypeFilter = document.getElementById('assignment-type');
    
    console.log('DOM elements:', {
        viewButtons: viewButtons.length,
        dashboardContent: dashboardContent ? 'found' : 'not found',
        dateRangeFilter: dateRangeFilter ? 'found' : 'not found',
        assignmentTypeFilter: assignmentTypeFilter ? 'found' : 'not found'
    });
    
    // Current view state
    let currentView = 'student';
    
    // Charts objects to manage instances
    let studentPerformanceChart = null;
    let assignmentCategoriesChart = null;
    let cohortDistributionChart = null;
    let cohortAverageChart = null;
    let cohortHeatmapChart = null;
    
    // Sample student data (placeholder)
    const studentData = {
        name: "Jane Smith",
        id: "ST12345",
        overallScore: 85,
        improvement: 7.5,
        strengths: ["Critical Analysis", "Research Methods", "Technical Writing"],
        weaknesses: ["Time Management", "Statistical Analysis"],
        assignments: [
            {
                title: "Research Proposal",
                date: "2023-02-10",
                type: "assignment",
                score: 78,
                feedback: "Good structure, but needs more literature citations.",
                categories: {
                    "Research": 85,
                    "Analysis": 75,
                    "Writing": 80,
                    "Citations": 65
                }
            },
            {
                title: "Literature Review",
                date: "2023-02-24",
                type: "assignment",
                score: 82,
                feedback: "Excellent synthesis of sources, consider deeper critical analysis.",
                categories: {
                    "Research": 90,
                    "Analysis": 80,
                    "Writing": 85,
                    "Citations": 75
                }
            },
            {
                title: "Midterm Exam",
                date: "2023-03-15",
                type: "exam",
                score: 85,
                feedback: "Strong understanding of core concepts, some minor errors in application.",
                categories: {
                    "Knowledge": 90,
                    "Analysis": 82,
                    "Application": 78
                }
            },
            {
                title: "Data Analysis Project",
                date: "2023-04-05",
                type: "project",
                score: 88,
                feedback: "Excellent analysis and visualization. Methods well-explained.",
                categories: {
                    "Research": 85,
                    "Analysis": 92,
                    "Writing": 88,
                    "Data Viz": 90
                }
            },
            {
                title: "Weekly Quiz 1",
                date: "2023-04-12",
                type: "quiz",
                score: 75,
                feedback: "Review statistical concepts from chapter 5.",
                categories: {
                    "Knowledge": 75,
                    "Application": 75
                }
            },
            {
                title: "Weekly Quiz 2",
                date: "2023-04-19",
                type: "quiz",
                score: 85,
                feedback: "Good improvement on statistical concepts.",
                categories: {
                    "Knowledge": 85,
                    "Application": 85
                }
            },
            {
                title: "Final Project Draft",
                date: "2023-05-01",
                type: "project",
                score: 92,
                feedback: "Excellent work. Consider expanding discussion section.",
                categories: {
                    "Research": 95,
                    "Analysis": 90,
                    "Writing": 92,
                    "Citations": 88,
                    "Data Viz": 95
                }
            }
        ]
    };
    
    // Sample cohort data (placeholder)
    const cohortData = {
        size: 25,
        overallAverage: 82,
        improvement: 5.2,
        topPerformers: [
            { id: "ST54321", name: "Alex Johnson", average: 94 },
            { id: "ST65432", name: "Taylor Williams", average: 91 },
            { id: "ST76543", name: "Jordan Brown", average: 89 }
        ],
        students: [
            { id: "ST12345", name: "Jane Smith", scores: [78, 82, 85, 88, 75, 85, 92] },
            { id: "ST23456", name: "David Lee", scores: [65, 70, 75, 80, 85, 85, 88] },
            { id: "ST34567", name: "Emily Chen", scores: [90, 88, 92, 85, 95, 90, 94] },
            { id: "ST45678", name: "Michael Wang", scores: [82, 80, 85, 88, 80, 85, 90] },
            { id: "ST54321", name: "Alex Johnson", scores: [95, 92, 94, 90, 96, 93, 97] },
            { id: "ST65432", name: "Taylor Williams", scores: [88, 90, 92, 89, 91, 93, 94] },
            { id: "ST76543", name: "Jordan Brown", scores: [85, 87, 89, 88, 90, 91, 93] }
        ],
        assignmentNames: [
            "Research Proposal", 
            "Literature Review", 
            "Midterm", 
            "Data Analysis", 
            "Quiz 1", 
            "Quiz 2", 
            "Final Draft"
        ],
        categories: ["Research", "Analysis", "Writing", "Citations", "Data Viz"],
        categoryAverages: [
            [85, 80, 82, 78, 0],    // Research Proposal
            [88, 82, 85, 82, 0],    // Literature Review
            [90, 85, 88, 0, 0],     // Midterm
            [87, 90, 85, 0, 92],    // Data Analysis
            [82, 80, 0, 0, 0],      // Quiz 1
            [87, 85, 0, 0, 0],      // Quiz 2
            [92, 90, 94, 90, 95]    // Final Draft
        ]
    };
    
    // Initialize the dashboard
    initDashboard();
    
    // Add animation class when switching views
    viewButtons.forEach(button => {
        button.addEventListener('click', () => {
            const view = button.dataset.view;
            
            // Update active button and ARIA states
            viewButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            button.classList.add('active');
            button.setAttribute('aria-selected', 'true');
            
            // Set aria-controls for the dashboard content
            dashboardContent.setAttribute('aria-labelledby', `${view}-tab`);
            
            // Add transition effect to dashboard content
            dashboardContent.classList.add('transition-effect');
            
            // Change view after short delay for animation
            setTimeout(() => {
                currentView = view;
                renderDashboard();
                
                // Remove transition effect after render
                setTimeout(() => {
                    dashboardContent.classList.remove('transition-effect');
                    
                    // Set focus to the first focusable element in the view for keyboard users
                    const focusTarget = dashboardContent.querySelector('button, [tabindex="0"], a, input, select');
                    if (focusTarget) {
                        focusTarget.focus();
                    }
                }, 50);
            }, 150);
        });
        
        // Add keyboard handling for tabs
        button.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                e.preventDefault();
                
                const buttons = Array.from(viewButtons);
                const currentIndex = buttons.indexOf(button);
                const direction = e.key === 'ArrowLeft' ? -1 : 1;
                const nextIndex = (currentIndex + direction + buttons.length) % buttons.length;
                
                buttons[nextIndex].focus();
            } else if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                button.click();
            }
        });
    });
    
    // Enhanced event listeners for filters with debounce
    let filterTimeout = null;
    const handleFilterChange = () => {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            renderDashboard();
        }, 300);
    };
    
    dateRangeFilter.addEventListener('change', handleFilterChange);
    assignmentTypeFilter.addEventListener('change', handleFilterChange);
    
    // Initialize dashboard structure
    function initDashboard() {
        console.log('Initializing dashboard');
        // Replace loading placeholder with actual content structure
        dashboardContent.innerHTML = `
            <div id="student-view" class="dashboard-view" role="tabpanel" aria-labelledby="student-tab">
                <!-- Student view content will be added dynamically -->
            </div>
            
            <div id="cohort-view" class="dashboard-view" role="tabpanel" aria-labelledby="cohort-tab" hidden>
                <!-- Cohort view content will be added dynamically -->
            </div>
        `;
        
        // Initial render
        renderDashboard();
    }
    
    // Render the appropriate view
    function renderDashboard() {
        console.log('Rendering dashboard, current view:', currentView);
        const studentView = document.getElementById('student-view');
        const cohortView = document.getElementById('cohort-view');
        
        console.log('Views:', {
            studentView: studentView ? 'found' : 'not found',
            cohortView: cohortView ? 'found' : 'not found'
        });
        
        // Show/hide views based on current selection
        if (currentView === 'student') {
            studentView.removeAttribute('hidden');
            cohortView.setAttribute('hidden', '');
        } else {
            studentView.setAttribute('hidden', '');
            cohortView.removeAttribute('hidden');
        }
        
        // Update content based on filters
        const dateRange = dateRangeFilter.value;
        const assignmentType = assignmentTypeFilter.value;
        
        console.log('Filters:', { dateRange, assignmentType });
        
        // Render appropriate view
        try {
            if (currentView === 'student') {
                renderStudentView(studentView, dateRange, assignmentType);
            } else {
                renderCohortView(cohortView, dateRange, assignmentType);
            }
        } catch (error) {
            console.error('Error rendering dashboard:', error);
            dashboardContent.innerHTML = `
                <div class="error-message">
                    <h3>Error loading dashboard</h3>
                    <p>${error.message}</p>
                </div>
            `;
        }
    }
    
    // Render student view with charts and metrics
    function renderStudentView(container, dateRange, assignmentType) {
        // Filter data based on selected filters
        let filteredAssignments = filterStudentData(studentData.assignments, dateRange, assignmentType);
        
        // Calculate current metrics based on filtered data
        const currentMetrics = calculateStudentMetrics(filteredAssignments);
        
        // Create the student view structure
        container.innerHTML = `
            <div class="student-header">
                <h2>${studentData.name} <span class="student-id">${studentData.id}</span></h2>
                <div class="overall-metrics">
                    <div class="metric">
                        <span class="metric-value">${currentMetrics.averageScore}%</span>
                        <span class="metric-label">Average Score</span>
                    </div>
                    <div class="metric improvement">
                        <span class="metric-value">${currentMetrics.improvement > 0 ? '+' : ''}${currentMetrics.improvement}%</span>
                        <span class="metric-label">Improvement</span>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <!-- Performance Over Time Chart -->
                <div class="grid-col-8">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Performance Over Time</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="performance-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Strengths and Weaknesses -->
                <div class="grid-col-4">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Strengths & Areas for Improvement</h3>
                        </div>
                        <div class="strengths-weaknesses">
                            <div class="strengths">
                                <h4>Strengths</h4>
                                <ul>
                                    ${studentData.strengths.map(strength => `<li>${strength}</li>`).join('')}
                                </ul>
                            </div>
                            <div class="weaknesses">
                                <h4>Areas for Improvement</h4>
                                <ul>
                                    ${studentData.weaknesses.map(weakness => `<li>${weakness}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Recent Assignments -->
                <div class="grid-col-6">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Recent Assignments</h3>
                        </div>
                        <div class="recent-assignments">
                            ${filteredAssignments.length > 0 ? 
                                filteredAssignments.slice(-3).reverse().map(assignment => `
                                    <div class="assignment-item">
                                        <div class="assignment-header">
                                            <h4>${assignment.title}</h4>
                                            <span class="date">${formatDate(assignment.date)}</span>
                                        </div>
                                        <div class="assignment-details">
                                            <div class="score-badge" data-score="${assignment.score}">
                                                ${assignment.score}%
                                            </div>
                                            <div class="assignment-feedback">
                                                <p>${assignment.feedback || 'No specific feedback provided.'}</p>
                                            </div>
                                        </div>
                                    </div>
                                `).join('') 
                                : '<div class="no-data-message">No assignments in selected time period</div>'
                            }
                        </div>
                    </div>
                </div>
                
                <!-- Category Performance -->
                <div class="grid-col-6">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Performance by Category</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="categories-chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Initialize charts if there's data
        if (filteredAssignments.length > 0) {
            // Add a small delay to ensure DOM is updated before initializing charts
            console.log('Scheduling chart initialization after DOM update');
            setTimeout(() => {
                console.log('Starting delayed chart initialization');
                // Verify chart containers exist
                const performanceCanvas = document.getElementById('performance-chart');
                const categoriesCanvas = document.getElementById('categories-chart');
                
                console.log('Chart canvases found:', {
                    performanceChart: performanceCanvas ? 'found' : 'not found',
                    categoriesChart: categoriesCanvas ? 'found' : 'not found'
                });
                
                initStudentCharts(filteredAssignments);
            }, 100);
        } else {
            // Show no data message for charts
            const chartContainers = container.querySelectorAll('.chart-container');
            chartContainers.forEach(container => {
                container.innerHTML = '<div class="no-data-message">No data available for selected filters</div>';
            });
        }
    }
    
    // Calculate student metrics based on filtered assignments
    function calculateStudentMetrics(assignments) {
        // Default values if no assignments
        if (assignments.length === 0) {
            return {
                averageScore: 0,
                improvement: 0
            };
        }
        
        // Calculate average score
        const totalScore = assignments.reduce((sum, a) => sum + a.score, 0);
        const averageScore = Math.round(totalScore / assignments.length);
        
        // Calculate improvement (difference between latest and oldest assignment)
        let improvement = 0;
        if (assignments.length >= 2) {
            // Sort by date
            const sortedAssignments = [...assignments].sort((a, b) => new Date(a.date) - new Date(b.date));
            const oldestScore = sortedAssignments[0].score;
            const latestScore = sortedAssignments[sortedAssignments.length - 1].score;
            improvement = Math.round((latestScore - oldestScore) * 10) / 10;
        }
        
        return {
            averageScore,
            improvement
        };
    }
    
    // Initialize student performance charts
    function initStudentCharts(assignments) {
        console.log('Initializing student charts with', assignments.length, 'assignments');
        try {
            // Performance line chart
            const performanceCtx = document.getElementById('performance-chart');
            if (!performanceCtx) {
                console.error('Performance chart canvas not found');
                return;
            }
            
            const ctx = performanceCtx.getContext('2d');
            
            // Destroy previous chart instance if it exists
            if (studentPerformanceChart) {
                studentPerformanceChart.destroy();
            }
            
            studentPerformanceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: assignments.map(a => formatShortDate(a.date)),
                    datasets: [{
                        label: 'Score (%)',
                        data: assignments.map(a => a.score),
                        borderColor: 'rgb(52, 152, 219)',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                title: function(tooltipItems) {
                                    const idx = tooltipItems[0].dataIndex;
                                    return assignments[idx].title;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            min: 0,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
            
            // Categories bar chart
            const categoriesCtx = document.getElementById('categories-chart');
            if (!categoriesCtx) {
                console.error('Categories chart canvas not found');
                return;
            }
            
            const catCtx = categoriesCtx.getContext('2d');
            
            // Aggregate scores by category
            const categories = {};
            assignments.forEach(assignment => {
                Object.entries(assignment.categories).forEach(([category, score]) => {
                    if (!categories[category]) {
                        categories[category] = [];
                    }
                    categories[category].push(score);
                });
            });
            
            // Calculate average score for each category
            const categoryLabels = Object.keys(categories);
            const categoryScores = categoryLabels.map(category => {
                const scores = categories[category];
                return scores.reduce((sum, score) => sum + score, 0) / scores.length;
            });
            
            // Destroy previous chart instance if it exists
            if (assignmentCategoriesChart) {
                assignmentCategoriesChart.destroy();
            }
            
            assignmentCategoriesChart = new Chart(catCtx, {
                type: 'bar',
                data: {
                    labels: categoryLabels,
                    datasets: [{
                        label: 'Average Score (%)',
                        data: categoryScores,
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.7)',
                            'rgba(46, 204, 113, 0.7)',
                            'rgba(155, 89, 182, 0.7)',
                            'rgba(52, 73, 94, 0.7)',
                            'rgba(243, 156, 18, 0.7)',
                            'rgba(231, 76, 60, 0.7)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            min: 0,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error initializing student charts:', error);
        }
    }
    
    // Render cohort overview with charts and metrics
    function renderCohortView(container, dateRange, assignmentType) {
        // Filter data based on selected filters
        const filteredData = filterCohortData(cohortData, dateRange, assignmentType);
        
        // Create the cohort view structure
        container.innerHTML = `
            <div class="cohort-header">
                <h2>Cohort Overview</h2>
                <div class="overall-metrics">
                    <div class="metric">
                        <span class="metric-value">${filteredData.overallAverage}%</span>
                        <span class="metric-label">Class Average</span>
                    </div>
                    <div class="metric improvement">
                        <span class="metric-value">+${filteredData.improvement}%</span>
                        <span class="metric-label">Overall Improvement</span>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <!-- Grade Distribution Chart -->
                <div class="grid-col-6">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Grade Distribution</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="distribution-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Top Performers -->
                <div class="grid-col-6">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Top Performers</h3>
                        </div>
                        <div class="top-performers">
                            ${filteredData.topPerformers.map((student, index) => `
                                <div class="top-performer ${index === 0 ? 'top-performer-1' : ''}">
                                    <div class="performer-rank">${index + 1}</div>
                                    <div class="performer-info">
                                        <div class="performer-name">${student.name}</div>
                                        <div class="performer-id">${student.id}</div>
                                    </div>
                                    <div class="performer-score">${student.average}%</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                
                <!-- Cohort Average Over Time -->
                <div class="grid-col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Class Average Over Time</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="cohort-average-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Performance by Category -->
                <div class="grid-col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Performance by Category</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="heatmap-chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Initialize charts
        console.log('Scheduling cohort chart initialization after DOM update');
        setTimeout(() => {
            console.log('Starting delayed cohort chart initialization');
            
            // Verify chart containers exist
            const distributionCanvas = document.getElementById('distribution-chart');
            const averageCanvas = document.getElementById('cohort-average-chart');
            const heatmapCanvas = document.getElementById('heatmap-chart');
            
            console.log('Cohort chart canvases found:', {
                distributionChart: distributionCanvas ? 'found' : 'not found',
                averageChart: averageCanvas ? 'found' : 'not found',
                heatmapChart: heatmapCanvas ? 'found' : 'not found'
            });
            
            initCohortCharts(filteredData);
        }, 100);
    }
    
    // Filter cohort data based on selected filters
    function filterCohortData(data, dateRange, assignmentType) {
        console.log('Filtering cohort data with filters:', { dateRange, assignmentType });
        
        // For this prototype, we'll simply return the entire cohort data
        // In a real application, this would apply filtering based on the date range and assignment type
        
        // Calculate top performers
        const topPerformers = calculateTopPerformers(data.students);
        
        // Calculate cohort average
        const { average, improvement } = calculateCohortAverage(data.students, data.assignmentNames);
        
        return {
            ...data,
            topPerformers: topPerformers,
            overallAverage: average || data.overallAverage, // Fallback to original data if calculation returns 0
            improvement: improvement || data.improvement    // Fallback to original data if calculation returns 0
        };
    }
    
    // Calculate top performers based on a set of students and their scores
    function calculateTopPerformers(students) {
        const studentsWithAvg = students.map(student => {
            const avg = student.scores.reduce((sum, score) => sum + score, 0) / 
                         (student.scores.length || 1);
            return {
                id: student.id,
                name: student.name,
                average: Math.round(avg * 10) / 10
            };
        });
        
        // Sort by average score (descending)
        studentsWithAvg.sort((a, b) => b.average - a.average);
        
        // Get top 3 (or fewer if we don't have enough)
        return studentsWithAvg.slice(0, 3);
    }
    
    // Calculate cohort average and improvement
    function calculateCohortAverage(students, assignmentNames) {
        if (!students.length || !students[0].scores.length) {
            return { average: 0, improvement: 0 };
        }
        
        // Calculate overall average
        let totalSum = 0;
        let count = 0;
        
        students.forEach(student => {
            student.scores.forEach(score => {
                totalSum += score;
                count++;
            });
        });
        
        const average = Math.round((totalSum / count) * 10) / 10;
        
        // Calculate improvement (first to last assignment)
        let improvement = 0;
        
        if (assignmentNames.length >= 2) {
            const firstAssignmentScores = students.map(s => s.scores[0]);
            const lastAssignmentScores = students.map(s => s.scores[s.scores.length - 1]);
            
            const firstAvg = firstAssignmentScores.reduce((sum, score) => sum + score, 0) / 
                              firstAssignmentScores.length;
            const lastAvg = lastAssignmentScores.reduce((sum, score) => sum + score, 0) / 
                             lastAssignmentScores.length;
            
            improvement = Math.round((lastAvg - firstAvg) * 10) / 10;
        }
        
        return { average, improvement };
    }
    
    // Initialize cohort overview charts
    function initCohortCharts(data) {
        // Grade distribution chart (histogram)
        const distributionCtx = document.getElementById('distribution-chart');
        if (!distributionCtx) {
            console.error('Distribution chart canvas not found');
            return;
        }
        const distCtx = distributionCtx.getContext('2d');
        
        // Calculate student averages and group into grade bands
        const averages = data.students.map(student => 
            student.scores.reduce((sum, score) => sum + score, 0) / student.scores.length
        );
        
        const gradeBands = [
            { min: 90, max: 100, label: 'A', color: 'rgba(46, 204, 113, 0.7)' },
            { min: 80, max: 89, label: 'B', color: 'rgba(52, 152, 219, 0.7)' },
            { min: 70, max: 79, label: 'C', color: 'rgba(243, 156, 18, 0.7)' },
            { min: 60, max: 69, label: 'D', color: 'rgba(231, 76, 60, 0.7)' },
            { min: 0, max: 59, label: 'F', color: 'rgba(149, 165, 166, 0.7)' }
        ];
        
        const gradeCounts = gradeBands.map(band => 
            averages.filter(avg => avg >= band.min && avg <= band.max).length
        );
        
        // Destroy previous chart instance if it exists
        if (cohortDistributionChart) {
            cohortDistributionChart.destroy();
        }
        
        cohortDistributionChart = new Chart(distCtx, {
            type: 'bar',
            data: {
                labels: gradeBands.map(band => band.label),
                datasets: [{
                    label: 'Number of Students',
                    data: gradeCounts,
                    backgroundColor: gradeBands.map(band => band.color),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Students'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Grade'
                        }
                    }
                }
            }
        });
        
        // Class average over time chart
        const averageCtx = document.getElementById('cohort-average-chart');
        if (!averageCtx) {
            console.error('Cohort average chart canvas not found');
            return;
        }
        const avgCtx = averageCtx.getContext('2d');
        
        // Calculate average scores for each assignment
        const assignmentAverages = data.assignmentNames.map((name, idx) => {
            const scores = data.students.map(student => student.scores[idx]);
            return scores.reduce((sum, score) => sum + score, 0) / scores.length;
        });
        
        // Destroy previous chart instance if it exists
        if (cohortAverageChart) {
            cohortAverageChart.destroy();
        }
        
        cohortAverageChart = new Chart(avgCtx, {
            type: 'line',
            data: {
                labels: data.assignmentNames,
                datasets: [{
                    label: 'Class Average (%)',
                    data: assignmentAverages,
                    borderColor: 'rgb(52, 152, 219)',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 50,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Performance by category heatmap
        const heatmapCtx = document.getElementById('heatmap-chart');
        if (!heatmapCtx) {
            console.error('Heatmap chart canvas not found');
            return;
        }
        const hmCtx = heatmapCtx.getContext('2d');
        
        // Destroy previous chart instance if it exists
        if (cohortHeatmapChart) {
            cohortHeatmapChart.destroy();
        }
        
        // Using a specialized plugin for heatmap would be ideal
        // For this prototype, we'll use a bar chart with conditional coloring
        const categoryData = data.categories.map((category, catIdx) => {
            return {
                label: category,
                data: data.categoryAverages.map(assignmentCats => assignmentCats[catIdx]),
                backgroundColor: getHeatmapColor,
                barPercentage: 1.0,
                categoryPercentage: 1.0
            };
        });
        
        cohortHeatmapChart = new Chart(hmCtx, {
            type: 'bar',
            data: {
                labels: data.assignmentNames,
                datasets: categoryData
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                scales: {
                    x: {
                        stacked: true,
                        display: false
                    },
                    y: {
                        stacked: true,
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                return `${context.dataset.label}: ${value}%`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Helper function to get heatmap color based on value
    function getHeatmapColor(context) {
        const value = context.raw;
        
        if (value >= 90) return 'rgba(46, 204, 113, 0.7)'; // Green (excellent)
        if (value >= 80) return 'rgba(52, 152, 219, 0.7)'; // Blue (good)
        if (value >= 70) return 'rgba(243, 156, 18, 0.7)'; // Yellow (average)
        if (value >= 60) return 'rgba(231, 76, 60, 0.7)'; // Red (poor)
        return 'rgba(149, 165, 166, 0.7)'; // Gray (very poor)
    }
    
    // Filter student data based on selected filters
    function filterStudentData(assignments, dateRange, assignmentType) {
        let filteredData = [...assignments];
        
        // Apply date filter
        if (dateRange !== 'all') {
            const now = new Date();
            let startDate = new Date();
            
            switch (dateRange) {
                case 'week':
                    startDate.setDate(now.getDate() - 7);
                    break;
                case 'month':
                    startDate.setMonth(now.getMonth() - 1);
                    break;
                case 'semester':
                    startDate.setMonth(now.getMonth() - 4);
                    break;
                case 'year':
                    startDate.setFullYear(now.getFullYear() - 1);
                    break;
            }
            
            filteredData = filteredData.filter(a => new Date(a.date) >= startDate);
        }
        
        // Apply assignment type filter
        if (assignmentType !== 'all') {
            filteredData = filteredData.filter(a => a.type === assignmentType);
        }
        
        // Sort by date (newest first)
        filteredData.sort((a, b) => new Date(a.date) - new Date(b.date));
        
        return filteredData;
    }
    
    // Helper functions
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }
    
    function formatShortDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});

// Add outside of the DOMContentLoaded event to check if script is loaded at all
console.log('Dashboard script file loaded'); 