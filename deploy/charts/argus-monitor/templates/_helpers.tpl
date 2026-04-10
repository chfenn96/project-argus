{{/* Define the name of the chart */}}
{{- define "project-argus-monitor.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Define a fully qualified app name */}}
{{- define "project-argus-monitor.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/* Common labels */}}
{{- define "project-argus-monitor.labels" -}}
helm.sh/chart: {{ include "project-argus-monitor.name" . }}
{{ include "project-argus-monitor.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Selector labels */}}
{{- define "project-argus-monitor.selectorLabels" -}}
app.kubernetes.io/name: {{ include "project-argus-monitor.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}