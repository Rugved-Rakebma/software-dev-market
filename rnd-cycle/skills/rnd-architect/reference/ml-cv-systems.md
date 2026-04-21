# ML/CV Specialist

Provides specialized guidance for machine learning and computer vision system design, model selection, and production deployment.

## When to Use

- Selecting ML models for specific use cases
- Designing training and inference pipelines
- Optimizing ML system performance and cost
- Evaluating build vs. API for ML capabilities
- Planning data pipelines for ML workloads

## ML System Design Framework

### Model Selection Decision Tree

```
Use Case Identified
    │
    ├─► Text/Language Tasks
    │   ├─► Classification → BERT, DistilBERT, or API (OpenAI, Claude)
    │   ├─► Generation → GPT-4, Claude, Llama (self-hosted)
    │   ├─► Embeddings → OpenAI Ada, sentence-transformers
    │   └─► Search/RAG → Vector DB + Embeddings + LLM
    │
    ├─► Computer Vision Tasks
    │   ├─► Classification → ResNet, EfficientNet, ViT
    │   ├─► Object Detection → YOLOv8, DETR, Faster R-CNN
    │   ├─► Segmentation → SAM, Mask R-CNN, U-Net
    │   ├─► OCR → Tesseract, PaddleOCR, Cloud Vision API
    │   └─► Face Recognition → InsightFace, DeepFace
    │
    ├─► Audio Tasks
    │   ├─► Speech-to-Text → Whisper, DeepSpeech, Cloud APIs
    │   ├─► Text-to-Speech → ElevenLabs, Coqui TTS
    │   └─► Audio Classification → PANNs, AudioSet models
    │
    └─► Structured Data
        ├─► Tabular → XGBoost, LightGBM, CatBoost
        ├─► Time Series → Prophet, ARIMA, Transformer-based
        └─► Recommendations → Two-tower, matrix factorization
```

---

## API vs. Self-Hosted Decision

### When to Use APIs

| Factor | API Preferred | Self-Hosted Preferred |
|--------|---------------|----------------------|
| **Volume** | < 10K requests/month | > 100K requests/month |
| **Latency** | > 500ms acceptable | < 100ms required |
| **Customization** | General use case | Domain-specific fine-tuning |
| **Data Privacy** | Non-sensitive data | PII, HIPAA, financial |
| **Team Expertise** | No ML engineers | ML team available |
| **Budget** | Predictable per-call costs | High volume justifies infra |

### Cost Comparison Framework

```markdown
## API Costs (Example: OpenAI GPT-4)
- Input: $0.03/1K tokens
- Output: $0.06/1K tokens
- Average request: 500 input + 200 output tokens
- Cost per request: $0.027
- 100K requests/month: $2,700

## Self-Hosted Costs (Example: Llama 70B)
- GPU instance: $3/hour (A100 40GB)
- Throughput: ~50 requests/minute = 3K/hour
- Cost per request: $0.001
- 100K requests/month: $100 + $500 engineering time

## Break-even Analysis
- < 50K requests: API likely cheaper
- > 50K requests: Self-hosted may be cheaper
- Factor in: engineering time, ops burden, model quality
```

---

## Training Pipeline Architecture

### Standard ML Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
├─────────────────────────────────────────────────────────────┤
│  Data Sources → ETL → Feature Store → Training Data         │
│  (S3, DBs)     (Airflow)  (Feast)     (Versioned)          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  TRAINING LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  Experiment Tracking → Training Jobs → Model Registry       │
│  (MLflow, W&B)         (SageMaker)    (MLflow, S3)         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  SERVING LAYER                               │
├─────────────────────────────────────────────────────────────┤
│  Model Server → Load Balancer → Monitoring                  │
│  (TorchServe)   (K8s/ELB)      (Prometheus)                │
└─────────────────────────────────────────────────────────────┘
```

### Component Selection Guide

| Component | Options | Recommendation |
|-----------|---------|----------------|
| **Feature Store** | Feast, Tecton, SageMaker | Feast (open source), Tecton (enterprise) |
| **Experiment Tracking** | MLflow, Weights & Biases, Neptune | MLflow (free), W&B (best UX) |
| **Training Orchestration** | Kubeflow, SageMaker, Vertex AI | SageMaker (AWS), Vertex (GCP) |
| **Model Registry** | MLflow, SageMaker, custom S3 | MLflow (standard) |
| **Model Serving** | TorchServe, TFServing, Triton | Triton (multi-framework) |

---

## Inference Architecture Patterns

### Pattern 1: Synchronous API

Best for: Low-latency requirements, simple integration

```
Client → API Gateway → Model Server → Response
                           │
                      Load Balancer
                           │
                    ┌──────┴──────┐
                    │             │
                Model Pod    Model Pod
```

**Latency targets**:
- P50: < 100ms
- P95: < 300ms
- P99: < 500ms

### Pattern 2: Asynchronous Processing

Best for: Long-running inference, batch processing

```
Client → API → Queue (SQS) → Worker → Result Store → Webhook/Poll
                                          │
                                     S3/Redis
```

**Use when**:
- Inference > 5 seconds
- Batch processing required
- Variable load patterns

### Pattern 3: Edge Inference

Best for: Privacy, offline capability, ultra-low latency

```
┌─────────────────────────────────────────┐
│              EDGE DEVICE                 │
│  ┌─────────┐    ┌─────────────────────┐ │
│  │ Camera  │───▶│ Optimized Model     │ │
│  └─────────┘    │ (ONNX, TFLite)      │ │
│                 └─────────────────────┘ │
│                          │              │
│                     Local Result        │
└─────────────────────────────────────────┘
                           │
                    Sync to Cloud
                    (non-blocking)
```

**Model optimization for edge**:
- Quantization (INT8): 4x smaller, 2-3x faster
- Pruning: 50-90% sparsity possible
- Distillation: Smaller model, similar accuracy
- ONNX/TFLite: Optimized runtime

---

## Computer Vision Pipeline Design

### Real-Time Video Processing

```
Camera Stream → Frame Extraction → Preprocessing → Model → Postprocessing → Output
     │              │                   │            │           │
   RTSP/         1-30 FPS           Resize,      Batch or    NMS, tracking,
   WebRTC                           normalize    single       annotation
```

**Performance optimization**:
- Process every Nth frame (skip frames)
- Resize to model input size early
- Batch frames when latency allows
- Use GPU preprocessing (NVIDIA DALI)

### Object Detection System

```markdown
## Pipeline Components

1. **Input Processing**
   - Video decode: FFmpeg, OpenCV
   - Frame buffer: Ring buffer for temporal context
   - Preprocessing: NVIDIA DALI (GPU), OpenCV (CPU)

2. **Detection**
   - Model: YOLOv8 (speed), DETR (accuracy)
   - Batch size: 1-8 depending on latency requirements
   - Confidence threshold: 0.5-0.7 typical

3. **Post-processing**
   - NMS (Non-Maximum Suppression)
   - Tracking: SORT, DeepSORT, ByteTrack
   - Smoothing: Kalman filter for stable boxes

4. **Output**
   - Annotations: Bounding boxes, labels, confidence
   - Events: Trigger on detection (webhook, queue)
   - Storage: Frame + metadata to S3/DB
```

---

## LLM Integration Patterns

### RAG (Retrieval-Augmented Generation)

```
User Query → Embedding → Vector Search → Context Retrieval → LLM → Response
                              │
                         Vector DB
                       (Pinecone, Weaviate,
                        Chroma, pgvector)
```

**Vector DB Selection**:
| Database | Best For | Limitations |
|----------|----------|-------------|
| **Pinecone** | Managed, scale | Cost at scale |
| **Weaviate** | Self-hosted, features | Operational overhead |
| **Chroma** | Simple, local dev | Not for production scale |
| **pgvector** | PostgreSQL users | Performance at >1M vectors |
| **Qdrant** | Performance | Newer, smaller community |

### LLM Serving Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY                               │
│  Rate limiting, auth, request routing                       │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │ GPT-4  │   │ Claude │   │ Local  │
         │  API   │   │  API   │   │ Llama  │
         └────────┘   └────────┘   └────────┘
                            │
                    Model Router
              (cost/latency/capability)
```

**Multi-model strategy**:
- Simple queries → Cheaper model (GPT-3.5, Haiku)
- Complex reasoning → Expensive model (GPT-4, Opus)
- Sensitive data → Self-hosted (Llama, Mistral)

---

## Performance Optimization

### GPU Memory Optimization

| Technique | Memory Reduction | Speed Impact |
|-----------|-----------------|--------------|
| **FP16 (Half Precision)** | 50% | Neutral to faster |
| **INT8 Quantization** | 75% | 10-20% slower |
| **INT4 Quantization** | 87.5% | 20-40% slower |
| **Gradient Checkpointing** | 60-80% | 20-30% slower |
| **Model Sharding** | Distributed | Communication overhead |

### Batching Strategies

```python
# Dynamic batching pseudocode
class DynamicBatcher:
    def __init__(self, max_batch=32, max_wait_ms=50):
        self.queue = []
        self.max_batch = max_batch
        self.max_wait = max_wait_ms

    async def add_request(self, request):
        self.queue.append(request)

        # Batch when full or timeout
        if len(self.queue) >= self.max_batch:
            return await self.process_batch()

        await asyncio.sleep(self.max_wait / 1000)
        return await self.process_batch()

    async def process_batch(self):
        batch = self.queue[:self.max_batch]
        self.queue = self.queue[self.max_batch:]
        return await self.model.predict_batch(batch)
```

---

## Model Monitoring

### Key Metrics to Track

| Metric | What It Measures | Alert Threshold |
|--------|------------------|-----------------|
| **Latency (P95)** | Response time | > 2x baseline |
| **Throughput** | Requests/second | < 80% capacity |
| **Error Rate** | Failed predictions | > 1% |
| **Model Drift** | Distribution shift | PSI > 0.2 |
| **Data Quality** | Input anomalies | > 5% anomalies |

### Drift Detection

```
Training Distribution ──┐
                        ├──► Statistical Test ──► Alert
Production Distribution ─┘
                         (PSI, KS test, JS divergence)
```

**Population Stability Index (PSI)**:
- PSI < 0.1: No significant change
- 0.1 < PSI < 0.2: Moderate change, monitor
- PSI > 0.2: Significant change, investigate

---

## Quick Reference Tables

### Model Selection by Use Case

| Use Case | Recommended Model | Latency | Cost |
|----------|-------------------|---------|------|
| Text Classification | DistilBERT | 10ms | Low |
| Text Generation | GPT-4 / Claude | 1-5s | Medium |
| Image Classification | EfficientNet-B0 | 5ms | Low |
| Object Detection | YOLOv8-n | 10ms | Low |
| Object Detection (Accurate) | YOLOv8-x | 50ms | Medium |
| Semantic Segmentation | SAM | 100ms | Medium |
| Speech-to-Text | Whisper-base | Real-time | Low |
| Embeddings | text-embedding-ada-002 | 50ms | Low |

### Infrastructure Sizing

| Scale | GPU | Model Size | Throughput |
|-------|-----|------------|------------|
| Development | T4 (16GB) | < 7B params | 10-50 req/s |
| Production Small | A10G (24GB) | < 13B params | 50-100 req/s |
| Production Medium | A100 (40GB) | < 70B params | 100-500 req/s |
| Production Large | A100 (80GB) x 2+ | > 70B params | 500+ req/s |

---

## Model Catalog

Comprehensive comparison of ML/CV models by category with performance benchmarks and use case recommendations.

---

### Large Language Models (LLMs)

#### API-Based Models

| Model | Provider | Context | Speed | Cost | Best For |
|-------|----------|---------|-------|------|----------|
| **GPT-4 Turbo** | OpenAI | 128K | Medium | $$$$ | Complex reasoning, code |
| **GPT-4o** | OpenAI | 128K | Fast | $$$ | Multimodal, general |
| **GPT-3.5 Turbo** | OpenAI | 16K | Fast | $ | Simple tasks, chat |
| **Claude 3 Opus** | Anthropic | 200K | Medium | $$$$ | Analysis, long context |
| **Claude 3.5 Sonnet** | Anthropic | 200K | Fast | $$ | Balanced quality/speed |
| **Claude 3 Haiku** | Anthropic | 200K | Very Fast | $ | High volume, simple |
| **Gemini Pro** | Google | 32K | Fast | $$ | Google ecosystem |

#### Open Source Models (Self-Hosted)

| Model | Parameters | VRAM | Speed | Quality | License |
|-------|------------|------|-------|---------|---------|
| **Llama 3 70B** | 70B | 140GB | Slow | Excellent | Meta |
| **Llama 3 8B** | 8B | 16GB | Fast | Good | Meta |
| **Mistral 7B** | 7B | 14GB | Fast | Good | Apache 2.0 |
| **Mixtral 8x7B** | 47B active | 90GB | Medium | Very Good | Apache 2.0 |
| **Phi-3 Mini** | 3.8B | 8GB | Very Fast | Good | MIT |
| **Qwen 2 72B** | 72B | 144GB | Slow | Excellent | Apache 2.0 |

#### LLM Selection Guide

```
Need reasoning/analysis?
├── YES → Budget available?
│   ├── YES → GPT-4 / Claude Opus
│   └── NO → Llama 70B / Mixtral (self-hosted)
│
└── NO → Simple chat/completion?
    ├── High volume → GPT-3.5 / Claude Haiku
    └── Data privacy → Llama 8B / Mistral 7B
```

---

### Computer Vision Models

#### Image Classification

| Model | Top-1 Accuracy | Params | Latency (GPU) | Best For |
|-------|----------------|--------|---------------|----------|
| **EfficientNet-B0** | 77.1% | 5.3M | 3ms | Mobile/edge |
| **EfficientNet-B4** | 82.9% | 19M | 8ms | Balanced |
| **EfficientNet-B7** | 84.3% | 66M | 25ms | High accuracy |
| **ResNet-50** | 76.1% | 25M | 5ms | Standard baseline |
| **ResNet-152** | 78.3% | 60M | 15ms | Higher accuracy |
| **ViT-B/16** | 81.8% | 86M | 10ms | Modern, attention-based |
| **ConvNeXt-Base** | 83.8% | 89M | 12ms | SOTA CNN |

#### Object Detection

| Model | mAP (COCO) | Params | FPS (V100) | Best For |
|-------|------------|--------|------------|----------|
| **YOLOv8-n** | 37.3% | 3.2M | 200+ | Real-time, edge |
| **YOLOv8-s** | 44.9% | 11.2M | 150+ | Balanced |
| **YOLOv8-m** | 50.2% | 25.9M | 100+ | Good accuracy |
| **YOLOv8-l** | 52.9% | 43.7M | 60+ | High accuracy |
| **YOLOv8-x** | 53.9% | 68.2M | 40+ | Best accuracy |
| **DETR** | 42.0% | 41M | 28 | Transformer-based |
| **RT-DETR-L** | 53.0% | 32M | 100+ | Real-time transformer |

#### Segmentation

| Model | Type | mIoU | Speed | Best For |
|-------|------|------|-------|----------|
| **SAM (ViT-H)** | Instance/Semantic | N/A | 50ms | Zero-shot, interactive |
| **SAM (ViT-B)** | Instance/Semantic | N/A | 15ms | Faster SAM |
| **Mask R-CNN** | Instance | 38.2% | 100ms | Standard instance seg |
| **U-Net** | Semantic | Varies | 20ms | Medical imaging |
| **DeepLabV3+** | Semantic | 82.1% | 30ms | High accuracy |
| **SegFormer-B5** | Semantic | 84.0% | 25ms | Transformer-based |

#### Face Recognition

| Model | LFW Accuracy | Speed | Features |
|-------|--------------|-------|----------|
| **InsightFace (ArcFace)** | 99.83% | 10ms | Industry standard |
| **DeepFace** | 99.65% | 15ms | Easy integration |
| **FaceNet** | 99.63% | 12ms | Google, well-documented |
| **RetinaFace** | Detection + landmarks | 30ms | Accurate detection |

---

### Speech & Audio Models

#### Speech-to-Text

| Model | WER (LibriSpeech) | Speed | Languages | Best For |
|-------|-------------------|-------|-----------|----------|
| **Whisper Large-v3** | 2.0% | 0.5x real-time | 99 | Best quality |
| **Whisper Medium** | 2.9% | 1x real-time | 99 | Balanced |
| **Whisper Small** | 3.4% | 2x real-time | 99 | Fast |
| **Whisper Tiny** | 5.6% | 4x real-time | 99 | Edge/mobile |
| **DeepSpeech** | 5.0% | 1x real-time | EN only | Lightweight |
| **Google Speech API** | ~2% | Real-time | 125+ | Managed, reliable |
| **AWS Transcribe** | ~3% | Real-time | 100+ | AWS ecosystem |

#### Text-to-Speech

| Model | Quality | Speed | Voices | Best For |
|-------|---------|-------|--------|----------|
| **ElevenLabs** | Excellent | Fast | Cloning | Most realistic |
| **OpenAI TTS** | Very Good | Fast | 6 | Simple integration |
| **Coqui TTS** | Good | Medium | Many | Open source |
| **Google TTS** | Good | Fast | 200+ | Multi-language |
| **Amazon Polly** | Good | Fast | 60+ | AWS ecosystem |

---

### Embedding Models

#### Text Embeddings

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| **text-embedding-3-large** | 3072 | Fast | Best | $0.13/1M tokens |
| **text-embedding-3-small** | 1536 | Very Fast | Good | $0.02/1M tokens |
| **text-embedding-ada-002** | 1536 | Fast | Good | $0.10/1M tokens |
| **sentence-transformers/all-MiniLM-L6** | 384 | Very Fast | Good | Free |
| **sentence-transformers/all-mpnet-base** | 768 | Fast | Very Good | Free |
| **Cohere embed-v3** | 1024 | Fast | Very Good | $0.10/1M tokens |

#### Image Embeddings

| Model | Dimensions | Use Case |
|-------|------------|----------|
| **CLIP ViT-B/32** | 512 | Text-image matching |
| **CLIP ViT-L/14** | 768 | Higher quality |
| **DINOv2** | 384-1536 | Visual similarity |
| **ResNet-50 features** | 2048 | Image retrieval |

---

### Structured Data Models

#### Tabular/Regression

| Model | Type | Best For | Training Speed |
|-------|------|----------|----------------|
| **XGBoost** | Gradient Boosting | General tabular | Fast |
| **LightGBM** | Gradient Boosting | Large datasets | Very Fast |
| **CatBoost** | Gradient Boosting | Categorical features | Fast |
| **Random Forest** | Ensemble | Baseline, interpretable | Medium |
| **TabNet** | Deep Learning | End-to-end learning | Slow |

#### Time Series

| Model | Type | Best For |
|-------|------|----------|
| **Prophet** | Additive | Business metrics, seasonality |
| **ARIMA** | Statistical | Short-term, stationary |
| **LSTM** | Deep Learning | Complex patterns |
| **Temporal Fusion Transformer** | Deep Learning | Multi-horizon |
| **N-BEATS** | Deep Learning | Univariate forecasting |

#### Recommendation Systems

| Model | Type | Best For |
|-------|------|----------|
| **Two-Tower** | Neural | Large-scale retrieval |
| **Matrix Factorization** | Collaborative | Simple, interpretable |
| **Wide & Deep** | Hybrid | Google-style recommendations |
| **BERT4Rec** | Sequential | Session-based |
| **Graph Neural Networks** | Graph | Social/network data |

---

### Model Optimization Techniques

#### Quantization Comparison

| Technique | Model Size | Speed | Accuracy Loss | VRAM |
|-----------|------------|-------|---------------|------|
| **FP32 (baseline)** | 100% | 1x | 0% | 100% |
| **FP16** | 50% | 1.5-2x | < 0.1% | 50% |
| **INT8** | 25% | 2-3x | 0.5-1% | 25% |
| **INT4** | 12.5% | 3-4x | 1-3% | 12.5% |
| **GPTQ** | 12.5% | 2-3x | 0.5-2% | 12.5% |
| **AWQ** | 12.5% | 3-4x | 0.3-1% | 12.5% |

#### Framework Selection

| Framework | Best For | Deployment |
|-----------|----------|------------|
| **PyTorch** | Research, flexibility | TorchServe, ONNX |
| **TensorFlow** | Production, enterprise | TF Serving, TFLite |
| **JAX** | Research, TPU | FLAX, Orbax |
| **ONNX** | Cross-platform | ONNX Runtime |
| **TensorRT** | NVIDIA optimization | Maximum GPU perf |

---

### Cost-Performance Matrix

#### LLM Cost per 1M Tokens

| Model | Input | Output | Quality Score |
|-------|-------|--------|---------------|
| GPT-4 Turbo | $10 | $30 | 95 |
| GPT-4o | $5 | $15 | 93 |
| Claude 3 Opus | $15 | $75 | 96 |
| Claude 3.5 Sonnet | $3 | $15 | 92 |
| Claude 3 Haiku | $0.25 | $1.25 | 82 |
| GPT-3.5 Turbo | $0.50 | $1.50 | 78 |
| Llama 3 70B (self) | ~$0.10 | ~$0.10 | 88 |

#### GPU Cost per Hour

| GPU | Cloud Cost/hr | VRAM | Best For |
|-----|---------------|------|----------|
| T4 | $0.35-0.50 | 16GB | Inference, small models |
| A10G | $1.00-1.50 | 24GB | Medium models |
| A100 40GB | $3.00-4.00 | 40GB | Training, large models |
| A100 80GB | $4.00-5.00 | 80GB | Very large models |
| H100 | $8.00-12.00 | 80GB | Cutting edge |

---

### Quick Decision Tables

#### "I need to classify images"

| Your Situation | Recommendation |
|----------------|----------------|
| Mobile/edge deployment | EfficientNet-B0, MobileNetV3 |
| General web app | ResNet-50, EfficientNet-B4 |
| Need best accuracy | ConvNeXt-Large, ViT-L |
| Custom domains | Fine-tune EfficientNet-B4 |

#### "I need to detect objects"

| Your Situation | Recommendation |
|----------------|----------------|
| Real-time video | YOLOv8-n or YOLOv8-s |
| Security/surveillance | YOLOv8-m + DeepSORT tracking |
| High accuracy needed | YOLOv8-x or RT-DETR |
| Edge deployment | YOLOv8-n + TensorRT |

#### "I need text generation"

| Your Situation | Recommendation |
|----------------|----------------|
| Best quality, no budget limit | GPT-4 / Claude Opus |
| Good quality, cost-conscious | Claude Sonnet / GPT-4o |
| High volume, simple tasks | GPT-3.5 / Claude Haiku |
| Data privacy required | Llama 3 / Mistral (self-hosted) |
| Offline/air-gapped | Llama 3 8B quantized |
