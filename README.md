## TODO
- [ ] Ingest NDSI data from a reliable source
- [ ] Evaluate alternative snow datasets (e.g., MODIS, SentinelHub)
- [ ] Convert SNODAS `.dat` files to GeoTIFF using GDAL
- [ ] Build raster alignment and merging pipeline
- [ ] (More to come — currently in ingestion phase)

## Snow generation Pipeline
```
        ┌────────────────────┐
        │  User Query Date   │
        └────────┬───────────┘
                    │
        ┌───────────▼────────────┐
        │ Check for cached tiles │
        └──────┬─────────┬───────┘
            │         │
        [ Exists ]   [ Missing ]
        │              │
    ┌────▼─────┐   ┌────▼────────┐
    │ Serve it │   │ Begin fetch │
    └──────────┘   └────┬────────┘
                        │
    ┌───────────────────▼────────────────────┐
    │ Check local SNODAS + NDSI availability │
    └────┬────────────────────┬──────────────┘
        │                    │
[ Available ]         [ Not Available ]
        │                    │
        │         ┌─────────▼─────────┐
        │         │ Attempt download  │
        │         │ (fallback -1 day) │
        │         └─────────┬─────────┘
        │                   ▼
    ┌───▼──────────┐   ┌────▼─────────────┐
    │ SNODAS .dat  │   │ NDSI GeoTIFF     │
    │ + .hdr built │   │ (native or DIY)  │
    └────┬─────────┘   └────────┬─────────┘
            ▼                     ▼
    ┌──────────────┐     ┌──────────────┐
    │ Convert to    │     │ Align/resample│
    │ GeoTIFF (GDAL)│     │ projections   │
    └────┬──────────┘     └──────┬───────┘
            ▼                     ▼
        ┌─────────────────────────────┐
        │ Merge SNODAS + NDSI layers  │
        └────────────┬────────────────┘
                    ▼
            ┌────────────────┐
            │ Generate TMS   │
            │ tiles (/z/x/y) │
            └──────┬─────────┘
                    ▼
            ┌──────────────┐
            │ Archive &    │
            │ Serve result │
            └──────────────┘
```