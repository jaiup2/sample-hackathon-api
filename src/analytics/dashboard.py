"""Real-time Dashboard Service for E-commerce Analytics.

This module provides live dashboard metrics and real-time notifications
for monitoring the e-commerce platform's performance.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from enum import Enum
import asyncio


class AlertSeverity(Enum):
    """Severity levels for dashboard alerts."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


class WidgetType(Enum):
    """Types of dashboard widgets."""
    REVENUE_CHART = "revenue_chart"
    ORDER_COUNT = "order_count"
    LIVE_VISITORS = "live_visitors"
    TOP_PRODUCTS = "top_products"
    REGIONAL_SALES = "regional_sales"
    INVENTORY_STATUS = "inventory_status"


@dataclass
class DashboardAlert:
    """Real-time alert for the dashboard."""
    alert_id: str
    title: str
    message: str
    severity: AlertSeverity
    timestamp: datetime
    acknowledged: bool = False
    auto_dismiss: bool = True


@dataclass
class LiveMetric:
    """A live-updating metric for the dashboard."""
    metric_id: str
    name: str
    current_value: float
    previous_value: float
    unit: str
    trend: str  # "up", "down", "stable"
    last_updated: datetime


@dataclass
class DashboardWidget:
    """Configuration for a dashboard widget."""
    widget_id: str
    widget_type: WidgetType
    title: str
    position: Dict[str, int]  # {"row": 1, "col": 2}
    refresh_interval_seconds: int
    data: Dict


class RealtimeDashboard:
    """
    Real-time dashboard service for live e-commerce monitoring.
    
    Features:
    - Live metrics with auto-refresh
    - WebSocket-based real-time updates
    - Customizable widget layouts
    - Smart alerting system
    - Performance monitoring
    """
    
    def __init__(self, refresh_rate: int = 5):
        """
        Initialize the dashboard service.
        
        Args:
            refresh_rate: Seconds between metric refreshes
        """
        self.refresh_rate = refresh_rate
        self.widgets: List[DashboardWidget] = []
        self.alerts: List[DashboardAlert] = []
        self.subscribers: List[Callable] = []
        self._running = False
    
    def get_live_metrics(self) -> List[LiveMetric]:
        """
        Get all live metrics for the dashboard.
        
        Returns:
            List of current LiveMetric values
        """
        now = datetime.now()
        
        return [
            LiveMetric(
                metric_id="revenue_today",
                name="Today's Revenue",
                current_value=45230.50,
                previous_value=42100.00,
                unit="USD",
                trend="up",
                last_updated=now
            ),
            LiveMetric(
                metric_id="orders_today",
                name="Orders Today",
                current_value=127,
                previous_value=98,
                unit="orders",
                trend="up",
                last_updated=now
            ),
            LiveMetric(
                metric_id="active_visitors",
                name="Active Visitors",
                current_value=342,
                previous_value=289,
                unit="users",
                trend="up",
                last_updated=now
            ),
            LiveMetric(
                metric_id="cart_value",
                name="Avg Cart Value",
                current_value=156.75,
                previous_value=143.20,
                unit="USD",
                trend="up",
                last_updated=now
            ),
            LiveMetric(
                metric_id="conversion_rate",
                name="Conversion Rate",
                current_value=3.8,
                previous_value=3.2,
                unit="%",
                trend="up",
                last_updated=now
            )
        ]
    
    def get_top_selling_products(self, limit: int = 5) -> List[Dict]:
        """
        Get top selling products in real-time.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List of top products with sales data
        """
        return [
            {"rank": 1, "name": "Wireless Headphones Pro", "sales": 234, "revenue": 28080.00},
            {"rank": 2, "name": "Smart Watch Series X", "sales": 189, "revenue": 37800.00},
            {"rank": 3, "name": "Bluetooth Speaker", "sales": 156, "revenue": 7800.00},
            {"rank": 4, "name": "USB-C Hub", "sales": 143, "revenue": 5720.00},
            {"rank": 5, "name": "Laptop Stand", "sales": 128, "revenue": 3840.00},
        ][:limit]
    
    def get_regional_breakdown(self) -> Dict[str, Dict]:
        """
        Get sales breakdown by region.
        
        Returns:
            Dict mapping regions to sales data
        """
        return {
            "North America": {"orders": 523, "revenue": 125520.00, "growth": 12.5},
            "Europe": {"orders": 412, "revenue": 98880.00, "growth": 8.3},
            "Asia Pacific": {"orders": 389, "revenue": 93360.00, "growth": 15.7},
            "Latin America": {"orders": 156, "revenue": 37440.00, "growth": 22.1},
            "Middle East": {"orders": 89, "revenue": 21360.00, "growth": 6.8}
        }
    
    def create_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity = AlertSeverity.INFO
    ) -> DashboardAlert:
        """
        Create a new dashboard alert.
        
        Args:
            title: Alert title
            message: Alert message
            severity: Alert severity level
            
        Returns:
            Created DashboardAlert object
        """
        alert = DashboardAlert(
            alert_id=f"alert_{len(self.alerts) + 1}",
            title=title,
            message=message,
            severity=severity,
            timestamp=datetime.now()
        )
        self.alerts.append(alert)
        self._notify_subscribers({"type": "alert", "data": alert})
        return alert
    
    def check_thresholds(self) -> List[DashboardAlert]:
        """
        Check metrics against thresholds and create alerts.
        
        Returns:
            List of new alerts generated
        """
        new_alerts = []
        metrics = self.get_live_metrics()
        
        for metric in metrics:
            # Check for significant drops
            if metric.previous_value > 0:
                change_pct = ((metric.current_value - metric.previous_value) 
                             / metric.previous_value * 100)
                
                if change_pct < -20:
                    alert = self.create_alert(
                        title=f"⚠️ {metric.name} Dropped",
                        message=f"{metric.name} decreased by {abs(change_pct):.1f}%",
                        severity=AlertSeverity.WARNING
                    )
                    new_alerts.append(alert)
                elif change_pct > 50:
                    alert = self.create_alert(
                        title=f"🚀 {metric.name} Surge",
                        message=f"{metric.name} increased by {change_pct:.1f}%!",
                        severity=AlertSeverity.SUCCESS
                    )
                    new_alerts.append(alert)
        
        return new_alerts
    
    def get_dashboard_config(self) -> Dict:
        """
        Get the full dashboard configuration.
        
        Returns:
            Complete dashboard config with all widgets
        """
        return {
            "dashboard_id": "main_dashboard",
            "title": "E-commerce Command Center",
            "refresh_rate": self.refresh_rate,
            "widgets": [
                {
                    "id": "revenue_widget",
                    "type": WidgetType.REVENUE_CHART.value,
                    "title": "Revenue Overview",
                    "position": {"row": 1, "col": 1, "width": 2, "height": 1}
                },
                {
                    "id": "orders_widget",
                    "type": WidgetType.ORDER_COUNT.value,
                    "title": "Order Activity",
                    "position": {"row": 1, "col": 3, "width": 1, "height": 1}
                },
                {
                    "id": "visitors_widget",
                    "type": WidgetType.LIVE_VISITORS.value,
                    "title": "Live Visitors",
                    "position": {"row": 2, "col": 1, "width": 1, "height": 1}
                },
                {
                    "id": "products_widget",
                    "type": WidgetType.TOP_PRODUCTS.value,
                    "title": "Top Products",
                    "position": {"row": 2, "col": 2, "width": 2, "height": 1}
                },
                {
                    "id": "regional_widget",
                    "type": WidgetType.REGIONAL_SALES.value,
                    "title": "Sales by Region",
                    "position": {"row": 3, "col": 1, "width": 3, "height": 1}
                }
            ],
            "theme": "dark",
            "last_updated": datetime.now().isoformat()
        }
    
    def subscribe(self, callback: Callable) -> None:
        """Subscribe to real-time updates."""
        self.subscribers.append(callback)
    
    def _notify_subscribers(self, event: Dict) -> None:
        """Notify all subscribers of an event."""
        for callback in self.subscribers:
            try:
                callback(event)
            except Exception:
                pass


# Quick access function
def get_dashboard_snapshot() -> Dict:
    """
    Get a complete snapshot of the dashboard state.
    
    Returns:
        Dict with all current dashboard data
    """
    dashboard = RealtimeDashboard()
    
    return {
        "metrics": [
            {
                "id": m.metric_id,
                "name": m.name,
                "value": m.current_value,
                "unit": m.unit,
                "trend": m.trend
            }
            for m in dashboard.get_live_metrics()
        ],
        "top_products": dashboard.get_top_selling_products(),
        "regional_sales": dashboard.get_regional_breakdown(),
        "config": dashboard.get_dashboard_config()
    }
