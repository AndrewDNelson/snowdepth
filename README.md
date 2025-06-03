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


When downloading data from the NDSI, we need to consider the following:
Cloud coverage
Map coverage (is it using older data, or is it just empty? How do you remedy this?)
Is the NDSI already claculated, or do we need to calculate it ourselves?
Missing days. Do we fallback until there are days availabile? 