---
name: Performance Issue
about: Report performance problems or optimization opportunities
title: '[PERFORMANCE] '
labels: ['performance']
assignees: ''

---

**Performance Issue Description**
A clear description of the performance problem you're experiencing.

**Current Performance**
What are you currently experiencing?
- Response time: [e.g. 5 seconds]
- Memory usage: [e.g. 500MB]
- CPU usage: [e.g. 90%]
- API throughput: [e.g. 10 requests/second]

**Expected Performance**
What performance level do you expect?
- Target response time: [e.g. < 1 second]
- Expected memory usage: [e.g. < 200MB]
- Expected CPU usage: [e.g. < 50%]
- Target throughput: [e.g. 100 requests/second]

**Component Affected**
Which part of the system is slow?
- [ ] 🔥 Mojo data processing
- [ ] 📊 Streamlit dashboard
- [ ] 🌐 FastAPI backend
- [ ] 🗄️ Database operations
- [ ] 📡 Open-Meteo API calls
- [ ] 🎯 Data analytics
- [ ] Other (specify): ___________

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Hardware: [e.g. 8GB RAM, 4 CPU cores, SSD]
- Dataset size: [e.g. 1000 weather records]
- Concurrent users: [e.g. 1, 10, 100]

**Reproduction Steps**
1. Go to '...'
2. Execute '...'
3. Measure performance with '...'
4. Observe slow performance

**Measurements**
Please provide specific performance measurements:
```
# Example: time taken for operations
# Memory usage snapshots
# CPU profiling data
```

**Profiling Data (if available)**
If you have profiling data, please include it:
```
# Profiler output
# Benchmark results
# Performance traces
```

**Optimization Ideas**
Do you have suggestions for optimization?
- [ ] SIMD vectorization opportunities
- [ ] Memory allocation improvements
- [ ] Caching strategies
- [ ] Database query optimization
- [ ] API batching
- [ ] Algorithm improvements
- [ ] Other: ___________

**Impact**
How does this performance issue affect your usage?
- [ ] Blocks development
- [ ] Slows down analysis
- [ ] Affects user experience
- [ ] Prevents deployment
- [ ] Minor inconvenience

**Additional Context**
Any other relevant information about the performance issue.
