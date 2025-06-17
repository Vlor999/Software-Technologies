#!/usr/bin/env python3

import re
import statistics
from datetime import datetime
from typing import List, Dict, Optional, Any

def mean(values: list[Any]) -> float:
    return sum(values) / len(values) if values else 0.0

def median(values: list[Any]) -> float:
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 1:
        return sorted_values[mid]
    else:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2

class PowerMetricsAnalyzer:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.samples:list[Dict[str, Any]] = []
        self.cpu_power_samples:list[int] = []
        self.gpu_power_samples:list[int] = []
        self.combined_power_samples:list[int] = []
        self.timestamps:list[datetime] = []
        
    def parse_log(self):
        with open(self.log_file_path, 'r') as file:
            content = file.read()
        
        # Split into individual samples
        sample_pattern = r'\*\*\* Sampled system activity \((.*?)\) \(.*?\) \*\*\*(.*?)(?=\*\*\* Sampled system activity|\Z)'
        matches = re.findall(sample_pattern, content, re.DOTALL)
        
        for timestamp_str, sample_content in matches:
            sample_data:Dict[str, Any] | None = self.parse_sample(timestamp_str, sample_content)
            if sample_data:
                self.samples.append(sample_data)
                
    def parse_sample(self, timestamp_str: str, content: str) -> Optional[Dict[str, Any]]:
        """Parse individual sample data"""
        try:
            timestamp = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S %Y %z')
            
            cpu_power:int | None = self.extract_power(content, r'CPU Power: (\d+) mW')
            gpu_power:int | None = self.extract_power(content, r'GPU Power: (\d+) mW')
            combined_power = self.extract_power(content, r'Combined Power.*?: (\d+) mW')
            
            e_cluster_usage = self.extract_percentage(content, r'E-Cluster HW active residency:\s*([\d.]+)%')
            p0_cluster_usage = self.extract_percentage(content, r'P0-Cluster HW active residency:\s*([\d.]+)%')
            p1_cluster_usage = self.extract_percentage(content, r'P1-Cluster HW active residency:\s*([\d.]+)%')
            
            gpu_usage = self.extract_percentage(content, r'GPU HW active residency:\s*([\d.]+)%')
            
            sample_data:dict[str, Any] = {
                'timestamp': timestamp,
                'cpu_power': cpu_power,
                'gpu_power': gpu_power,
                'combined_power': combined_power,
                'e_cluster_usage': e_cluster_usage,
                'p0_cluster_usage': p0_cluster_usage,
                'p1_cluster_usage': p1_cluster_usage,
                'gpu_usage': gpu_usage
            }
            
            # Store for analysis
            if cpu_power is not None:
                self.cpu_power_samples.append(cpu_power)
            if gpu_power is not None:
                self.gpu_power_samples.append(gpu_power)
            if combined_power is not None:
                self.combined_power_samples.append(combined_power)
            
            self.timestamps.append(timestamp)
            
            return sample_data
            
        except Exception as e:
            print(f"Error parsing sample: {e}")
            return None
    
    def extract_power(self, content: str, pattern: str) -> Optional[int]:
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None
    
    def extract_percentage(self, content: str, pattern: str) -> Optional[float]:
        match = re.search(pattern, content)
        return float(match.group(1)) if match else None
    
    def analyze(self) -> Dict[str, Any]:
        if not self.samples:
            return {"error": "No samples found in log file"}
        
        analysis:Dict[str, Any] = {
            "execution_summary": self.analyze_execution_summary(),
            "power_consumption": self.analyze_power_consumption(),
            "cpu_analysis": self.analyze_cpu_usage(),
            "gpu_analysis": self.analyze_gpu_usage(),
            "energy_estimation": self.estimate_energy_consumption(),
            "performance_insights": self.analyze_performance_patterns(),
        }
        
        return analysis
    
    def analyze_execution_summary(self) -> Dict[str, Any]:
        if not self.timestamps:
            return {}
            
        duration = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        sample_count = len(self.samples)
        avg_interval = duration / (sample_count - 1) if sample_count > 1 else 0
        
        return {
            "total_duration_seconds": duration,
            "sample_count": sample_count,
            "average_sample_interval": round(avg_interval, 2),
            "start_time": self.timestamps[0].strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.timestamps[-1].strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def analyze_power_consumption(self) -> Dict[str, Any]:
        analysis:Dict[str, Any] = {}
        
        if self.cpu_power_samples:
            analysis["cpu_power"] = {
                "min_mw": min(self.cpu_power_samples),
                "max_mw": max(self.cpu_power_samples),
                "average_mw": round(mean(self.cpu_power_samples), 2),
                "median_mw": round(median(self.cpu_power_samples), 2),
                "std_dev": round(statistics.stdev(self.cpu_power_samples) if len(self.cpu_power_samples) > 1 else 0, 2)
            }
        
        if self.gpu_power_samples:
            analysis["gpu_power"] = {
                "min_mw": min(self.gpu_power_samples),
                "max_mw": max(self.gpu_power_samples),
                "average_mw": round(mean(self.gpu_power_samples), 2),
                "median_mw": round(median(self.gpu_power_samples), 2),
                "std_dev": round(statistics.stdev(self.gpu_power_samples) if len(self.gpu_power_samples) > 1 else 0, 2)
            }
        
        if self.combined_power_samples:
            analysis["combined_power"] = {
                "min_mw": min(self.combined_power_samples),
                "max_mw": max(self.combined_power_samples),
                "average_mw": round(mean(self.combined_power_samples), 2),
                "median_mw": round(median(self.combined_power_samples), 2),
                "std_dev": round(statistics.stdev(self.combined_power_samples) if len(self.combined_power_samples) > 1 else 0, 2)
            }
        
        return analysis
    
    def analyze_cpu_usage(self) -> Dict[str, Any]:
        e_cluster_usage: list[float] = [s['e_cluster_usage'] for s in self.samples if isinstance(s['e_cluster_usage'], (int, float))]
        p0_cluster_usage: list[float] = [s['p0_cluster_usage'] for s in self.samples if isinstance(s['p0_cluster_usage'], (int, float))]
        p1_cluster_usage: list[float] = [s['p1_cluster_usage'] for s in self.samples if isinstance(s['p1_cluster_usage'], (int, float))]
        
        analysis: Dict[str, Any] = {}
        
        if e_cluster_usage:
            analysis["e_cluster"] = {
                "average_usage_percent": round(mean(e_cluster_usage), 2),
                "max_usage_percent": round(max(e_cluster_usage), 2),
                "min_usage_percent": round(min(e_cluster_usage), 2)
            }
        
        if p0_cluster_usage:
            analysis["p0_cluster"] = {
                "average_usage_percent": round(mean(p0_cluster_usage), 2),
                "max_usage_percent": round(max(p0_cluster_usage), 2),
                "min_usage_percent": round(min(p0_cluster_usage), 2)
            }
        
        if p1_cluster_usage:
            analysis["p1_cluster"] = {
                "average_usage_percent": round(mean(p1_cluster_usage), 2),
                "max_usage_percent": round(max(p1_cluster_usage), 2),
                "min_usage_percent": round(min(p1_cluster_usage), 2)
            }
        
        return analysis
    
    def analyze_gpu_usage(self) -> Dict[str, Any]:
        gpu_usage = [s['gpu_usage'] for s in self.samples if s['gpu_usage'] is not None]
        
        if not gpu_usage:
            return {}
        
        return {
            "average_usage_percent": round(mean(gpu_usage), 2),
            "max_usage_percent": round(max(gpu_usage), 2),
            "min_usage_percent": round(min(gpu_usage), 2),
            "samples_with_gpu_activity": len([u for u in gpu_usage if u > 0])
        }
    
    def estimate_energy_consumption(self) -> Dict[str, Any]:
        if not self.combined_power_samples or not self.timestamps:
            return {}
        
        duration = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        avg_power_mw = mean(self.combined_power_samples)
        
        total_energy_mj = avg_power_mw * duration
        total_energy_j = total_energy_mj / 1000
        total_energy_wh = total_energy_j / 3600
        
        return {
            "total_energy_millijoules": round(total_energy_mj, 2),
            "total_energy_joules": round(total_energy_j, 4),
            "total_energy_watt_hours": round(total_energy_wh, 6),
            "average_power_watts": round(avg_power_mw / 1000, 3),
            "duration_seconds": duration
        }
    
    def analyze_performance_patterns(self) -> Dict[str, Any]:
        patterns:Dict[str, Any] = {}
        
        # Identify high-power phases
        if self.combined_power_samples:
            high_power_threshold = mean(self.combined_power_samples) * 1.5
            high_power_samples = [p for p in self.combined_power_samples if p > high_power_threshold]
            
            patterns["high_power_phases"] = {
                "threshold_mw": round(high_power_threshold, 2),
                "high_power_sample_count": len(high_power_samples),
                "percentage_of_execution": round(len(high_power_samples) / len(self.combined_power_samples) * 100, 2)
            }
        
        # Analyze power ramp-up and ramp-down
        if len(self.combined_power_samples) > 10:
            initial_samples = self.combined_power_samples[:5]
            final_samples = self.combined_power_samples[-5:]
            peak_samples = sorted(self.combined_power_samples, reverse=True)[:5]
            
            patterns["power_phases"] = {
                "initial_average_mw": round(mean(initial_samples), 2),
                "peak_average_mw": round(mean(peak_samples), 2),
                "final_average_mw": round(mean(final_samples), 2)
            }
        
        return patterns
    
    def _generate_recommendations(self) -> List[str]:
        recommendations:List[str] = []
        
        if self.combined_power_samples:
            avg_power = mean(self.combined_power_samples)
            max_power = max(self.combined_power_samples)
            
            # High power consumption
            if avg_power > 5000:  # > 5W
                recommendations.append("High average power consumption detected. Consider optimizing algorithm complexity.")
            
            # Power spikes
            if max_power > avg_power * 2:
                recommendations.append("Significant power spikes detected. Consider implementing workload balancing.")
        
        # CPU usage analysis
        cpu_analysis = self.analyze_cpu_usage()
        if 'p1_cluster' in cpu_analysis and cpu_analysis['p1_cluster']['average_usage_percent'] > 80:
            recommendations.append("High P-core usage detected. Consider parallel processing optimization.")
        
        # GPU usage analysis
        gpu_analysis = self.analyze_gpu_usage()
        if gpu_analysis and gpu_analysis['average_usage_percent'] < 5:
            recommendations.append("Low GPU utilization. Consider GPU acceleration for computational tasks.")
        
        # Energy efficiency
        energy_est = self.estimate_energy_consumption()
        if energy_est and energy_est['total_energy_joules'] > 100:
            recommendations.append("High energy consumption. Consider algorithm optimization or caching strategies.")
        
        if not recommendations:
            recommendations.append("Energy consumption appears optimized for this workload.")
        
        return recommendations
    
    def generate_report(self) -> str:
        analysis = self.analyze()
        
        report:list[str] = []
        report.append("=" * 80)
        report.append("POWERMETRICS ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Execution Summary
        if 'execution_summary' in analysis:
            exec_sum = analysis['execution_summary']
            report.append(f"\n📊 EXECUTION SUMMARY")
            report.append(f"Duration: {exec_sum.get('total_duration_seconds', 'N/A')} seconds")
            report.append(f"Samples collected: {exec_sum.get('sample_count', 'N/A')}")
            report.append(f"Average sampling interval: {exec_sum.get('average_sample_interval', 'N/A')} seconds")
            report.append(f"Execution period: {exec_sum.get('start_time', 'N/A')} → {exec_sum.get('end_time', 'N/A')}")
        
        # Power Consumption Analysis
        if 'power_consumption' in analysis:
            power = analysis['power_consumption']
            report.append(f"\n⚡ POWER CONSUMPTION ANALYSIS")
            
            if 'combined_power' in power:
                cp = power['combined_power']
                report.append(f"Total System Power:")
                report.append(f"  * Average: {cp['average_mw']} mW ({cp['average_mw']/1000:.3f} W)")
                report.append(f"  * Range: {cp['min_mw']} - {cp['max_mw']} mW")
                report.append(f"  * Variability (sigma): {cp['std_dev']} mW")
            
            if 'cpu_power' in power:
                cpu = power['cpu_power']
                report.append(f"CPU Power:")
                report.append(f"  * Average: {cpu['average_mw']} mW")
                report.append(f"  * Peak: {cpu['max_mw']} mW")
            
            if 'gpu_power' in power:
                gpu = power['gpu_power']
                report.append(f"GPU Power:")
                report.append(f"  * Average: {gpu['average_mw']} mW")
                report.append(f"  * Peak: {gpu['max_mw']} mW")
        
        # Energy Estimation
        if 'energy_estimation' in analysis:
            energy = analysis['energy_estimation']
            report.append(f"\n🔋 ENERGY CONSUMPTION ESTIMATE")
            report.append(f"Total Energy: {energy.get('total_energy_joules', 'N/A')} J ({energy.get('total_energy_watt_hours', 'N/A')} Wh)")
            report.append(f"Average Power: {energy.get('average_power_watts', 'N/A')} W")
            if energy.get('total_energy_watt_hours'):
                cost_estimate = energy['total_energy_watt_hours'] * 0.12  # Assuming $0.12/kWh
                report.append(f"Estimated cost (at $0.12/kWh): ${cost_estimate * 1000:.6f}")
        
        # CPU Analysis
        if 'cpu_analysis' in analysis:
            cpu = analysis['cpu_analysis']
            report.append(f"\n🖥️  CPU UTILIZATION ANALYSIS")
            
            if 'e_cluster' in cpu:
                report.append(f"E-cores (Efficiency): {cpu['e_cluster']['average_usage_percent']}% avg")
            if 'p0_cluster' in cpu:
                report.append(f"P0-cores (Performance): {cpu['p0_cluster']['average_usage_percent']}% avg")
            if 'p1_cluster' in cpu:
                report.append(f"P1-cores (Performance): {cpu['p1_cluster']['average_usage_percent']}% avg")
        
        # GPU Analysis
        if 'gpu_analysis' in analysis and analysis['gpu_analysis']:
            gpu = analysis['gpu_analysis']
            report.append(f"\n🎮 GPU UTILIZATION ANALYSIS")
            report.append(f"Average utilization: {gpu['average_usage_percent']}%")
            report.append(f"Peak utilization: {gpu['max_usage_percent']}%")
            report.append(f"Samples with GPU activity: {gpu['samples_with_gpu_activity']}")
        
        # Performance Patterns
        if 'performance_insights' in analysis:
            perf = analysis['performance_insights']
            report.append(f"\n📈 PERFORMANCE PATTERNS")
            
            if 'high_power_phases' in perf:
                hpp = perf['high_power_phases']
                report.append(f"High-power phases: {hpp['percentage_of_execution']}% of execution")
                report.append(f"High-power threshold: {hpp['threshold_mw']} mW")
            
            if 'power_phases' in perf:
                pp = perf['power_phases']
                report.append(f"Power progression:")
                report.append(f"  * Initial: {pp['initial_average_mw']} mW")
                report.append(f"  * Peak: {pp['peak_average_mw']} mW")
                report.append(f"  * Final: {pp['final_average_mw']} mW")
    
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)

def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python3 power_analyzer.py <power_log_file> <output_name>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    output_name = sys.argv[2]
    
    try:
        analyzer = PowerMetricsAnalyzer(log_file)
        analyzer.parse_log()
        
        if not analyzer.samples:
            print("❌ No valid samples found in the log file.")
            sys.exit(1)
        
        print(analyzer.generate_report())
        
        # Optionally save analysis to JSON
        import json
        analysis_data = analyzer.analyze()
        with open(output_name, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        print(f"\n📄 Detailed analysis saved to: power_analysis.json")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{log_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()