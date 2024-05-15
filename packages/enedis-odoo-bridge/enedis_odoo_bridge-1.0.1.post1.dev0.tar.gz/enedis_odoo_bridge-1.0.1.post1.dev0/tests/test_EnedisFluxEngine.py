import pytest
import secrets
import pandas as pd
from pandas import DataFrame
from enedis_odoo_bridge.EnedisFluxEngine import EnedisFluxEngine
@pytest.fixture
def setup_enedis_flux_engine():
    config = {
        'AES_KEY': secrets.token_hex(16 // 2),
        'AES_IV': secrets.token_hex(16 // 2),
        'FTP_USER': 'user',
        'FTP_PASSWORD': 'password',
        'FTP_ADDRESS': 'ftp.address.com',
        'FTP_R15_DIR': 'R15',
        'FTP_C15_DIR': 'C15',
        'FTP_F15_DIR': 'F15'
    }
    engine = EnedisFluxEngine(config=config, flux=['R15'])
    # Mocking R15 data
    engine.data = {
        'R15': DataFrame({
            'pdl': ['pdl1', 'pdl2'],
            'consumption': [100, 200],
            'additional_info': ['info1', 'info2']
        })
    }
    return engine

def test_enrich_estimates_with_existing_columns(setup_enedis_flux_engine):
    engine = setup_enedis_flux_engine
    estimates = DataFrame({
        'pdl': ['pdl1', 'pdl2'],
        'estimated_consumption': [90, 180]
    })
    columns_to_enrich = ['additional_info']
    enriched_estimates = engine.enrich_estimates(estimates, columns_to_enrich)
    
    assert 'additional_info' in enriched_estimates.columns, "The enriched DataFrame should contain the 'additional_info' column."
    assert all(enriched_estimates['additional_info'] == ['info1', 'info2']), "The values in the 'additional_info' column should match the R15 data."

def test_enrich_estimates_with_nonexistent_column(setup_enedis_flux_engine):
    engine = setup_enedis_flux_engine
    estimates = DataFrame({
        'pdl': ['pdl1', 'pdl2'],
        'estimated_consumption': [90, 180]
    })
    columns_to_enrich = ['nonexistent_column']
    
    with pytest.raises(ValueError) as excinfo:
        engine.enrich_estimates(estimates, columns_to_enrich)
    
    assert "Asked column nonexistent_column not found in R15 data." in str(excinfo.value), "A ValueError should be raised for a nonexistent column."